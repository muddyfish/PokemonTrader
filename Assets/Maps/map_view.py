import zipfile
import json
try:
  import cStringIO as StringIO
except ImportError:
  import StringIO
  
class Map():
  def __init__(self, main, pygame):
    globals()["main"] = main
    globals()["pygame"] = pygame
    self.noclip = 'noclip' in main.args
    self.screen = main.screen
    self.map_f = main.args[1]
    self.load_map(self.map_f)
    self.tile_offset = [0,0]
    self.view_offset = [0,0]
    self.coll_surf = pygame.Surface((16,16), pygame.SRCALPHA)
    self.coll_surf.fill((0,128,0,128))
    self.blit_range = [range(self.blit_tiles[i]) for i in [0,1]]
    self.move_directions = {pygame.K_LEFT: (0,-1),
			    pygame.K_RIGHT:(0, 1),
			    pygame.K_UP:   (1,-1),
			    pygame.K_DOWN: (1, 1)}
    self.current_direction = [0,0]
    self.pos = [[[[(self.get_pos(x,y, [x2,y2])) \
      for y in self.blit_range[1]] \
      for x in self.blit_range[0]] \
      for y2 in range(17)] \
      for x2 in range(17)]
    
  def reload_hashes(self):
    self.hash_dict = {'get_pos': {}}

  def load_map(self, map_f):
    self.reload_hashes()
    self.map = zipfile.ZipFile(map_f, "r")
    self.map_name = map_f.split("/")[-1]
    namelist = self.map.namelist()
    self.position = json.load(self.map.open("position"))
    self.tilesheet = pygame.image.load(StringIO.StringIO(self.map.read("tilesheet")), ".tga")
    if 'collision' in namelist:
      self.collision = json.load(self.map.open("collision"))
    else:
      self.collision = self.get_2darray(len(self.position[0])*2, len(self.position)*2)
    self.exits = {}
    if 'exits' in namelist:
      exits = json.load(self.map.open("exits"))
      for key in exits:
       self.exits[tuple(json.loads(key))] = exits[key]
    self.map.close()
    self.tile_size = self.tilesheet.get_height()
    self.tile_ims = []
    for tile in range(self.tilesheet.get_width()//self.tile_size):
      self.tile_ims.append(pygame.Surface((self.tile_size, self.tile_size)))
      self.tile_ims[-1].blit(self.tilesheet, (0,0), (tile*self.tile_size,0,(tile+1)*self.tile_size,16))
    self.tiles = [[self.tile_ims[self.position[x][y]] \
      for y in range(len(self.position[0]))] \
      for x in range(len(self.position))]
    self.blit_tiles = [i//self.tile_size+1 for i in self.screen.get_size()]
  
  def get_2darray(self, x, y, fill='0'):
    return [[int(fill) \
	for a in range(x)] \
	for b in range(y)]
  
  def get_pos(self, x, y, view_offset, mult=16):
    h = hash((x,y,view_offset[0],view_offset[1],mult))
    if h in self.hash_dict['get_pos']:
      return self.hash_dict['get_pos'][h]
    if mult > 8:
      rtn = ((x-1)*16+view_offset[0], (y-1)*16+view_offset[1])
    else:
      rtn = ((x-2)*16+view_offset[0], (y-2)*16+view_offset[1])
    self.hash_dict['get_pos'][h] = rtn
    return rtn

  def get_offset(self):
    return [self.tile_offset[i]*2-(self.view_offset[i]>>3)+self.blit_tiles[i] for i in range(2)] 

  def check_exits(self, d, a):
    offset = self.get_offset()
    for j in [0,1]:
      for i in [0,1]:
	cur_offset = (offset[0]-i,offset[1]-j)
	if cur_offset in self.exits:
	  e = self.exits[cur_offset]
	  if e[3]-1-e[3]%2!=a and e[3]%2==d:
	    return e
  
  def use_exit(self, exit):
    if exit == None: return
    filter_list = [exit[2], self.map_name, exit[0]]
    self.load_map('Assets/Maps/'+exit[1])
    offset = sorted([k for (k,v) in self.exits.iteritems() if filter_list == v[:3]])
    offset = offset[len(offset)/2]
    self.tile_offset = [offset[0]/2-self.blit_tiles[0]/2,offset[1]/2-self.blit_tiles[1]/2+2]
    self.view_offset = [((offset[0]+1)%2)*8,(offset[1]%2)*8]
    d=(self.exits[offset][3]-1)%2
    self.tile_offset[d^1]+={1:1,0:-1}[d]
    self.current_direction=[0,0]
    self.screen.blit_all()
    
  def collide(self, d, a):
    if self.noclip: return True
    offset = self.get_offset()
    offset[d]+=a
    return not (self.collision[offset[0]][offset[1]] or self.collision[offset[0]-1][offset[1]] or \
                self.collision[offset[0]][offset[1]-1] or self.collision[offset[0]-1][offset[1]-1])

  def move(self, d, a):
    if self.current_direction == [0,0] and self.collide(d,a):
      self.current_direction[d] = -2*a
      if len({(self.view_offset[d], a), (0,1), (16,0)})==2:
	self.tile_offset[d]+=a
	self.view_offset[d]=16
      self.view_offset[d]-=2*a
      self.use_exit(self.check_exits(d, a))
    elif self.current_direction == [0,0]:
      self.use_exit(self.check_exits(d, a))      

  def run(self, events):
    for event in events:
      if event.type == main.tick_event:
	if self.current_direction != [0,0]:
	  d = int(self.current_direction[1]!=0)
	  self.view_offset[d]+=self.current_direction[d]
	  if self.view_offset[d]==16:
	    self.tile_offset[d]-=self.current_direction[d]/2
	    self.view_offset[d]=0
	  if self.view_offset[d]%8==0:
	    self.current_direction = [0,0]
	  self.screen.blit_all()
      if event.type == pygame.KEYDOWN:
        if event.key in self.move_directions:
	  self.move(*self.move_directions[event.key])
    player_pos = [self.screen.get_width()/2-16, self.screen.get_height()/2-16]
    blit_x = self.tile_offset[0]
    blit_y = self.tile_offset[1]
    view_x = self.view_offset[0]
    view_y = self.view_offset[1]
    
    if self.tile_offset[0] < 0:
      blit_x = -1
      view_x = -16
      player_pos[0] += self.tile_offset[0]*16-self.view_offset[0]+16
    elif self.tile_offset[0]+self.blit_tiles[0]-1 >= len(self.tiles):
      blit_x = len(self.tiles)-self.blit_tiles[0]
      view_x = 0
      player_pos[0] -= (len(self.tiles)-self.blit_tiles[0]-self.tile_offset[0])*16+self.view_offset[0]
    if self.tile_offset[1] < 0:
      blit_y = -1
      view_y = -16
      player_pos[1] += self.tile_offset[1]*16-self.view_offset[1]+16
    elif self.tile_offset[1]+self.blit_tiles[1]-1 >= len(self.tiles[0]):
      blit_y = len(self.tiles[0])-self.blit_tiles[1]
      view_y = 0
      player_pos[1] -= (len(self.tiles[0])-self.blit_tiles[1]-self.tile_offset[1])*16+self.view_offset[1]
 
    for x in self.blit_range[0]:
      for y in self.blit_range[1]:
	self.screen.blit_func(self.tiles[blit_x+x][blit_y+y], self.pos[view_x][view_y][x][y])
    self.screen.blit_func(self.coll_surf, player_pos)
    
def add_globals(main, pygame):
  globals()["main"] = main
  globals()["pygame"] = pygame