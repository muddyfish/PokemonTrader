import zipfile
import json
try:
  import cStringIO as StringIO
except ImportError:
  import StringIO
  
class Map(object):
  def __init__(self, main, pygame, map_f):
    globals()["main"] = main
    globals()["pygame"] = pygame
    self.screen = main.screen
    self.asset_loader = main.asset_loader
    self.tile_offset = [0,0]
    self.view_offset = [8,8]
    self.current_direction = [0,0]
    self.load_map(map_f)
    self.blit_range = [range(self.blit_tiles[i]) for i in [0,1]]
    self.pos = [[[[(self.get_pos(x,y, 8, [x2,y2])) \
      for y in self.blit_range[1]] \
      for x in self.blit_range[0]] \
      for y2 in range(17)] \
      for x2 in range(17)]
    
  def reload_hashes(self):
    self.hash_dict = {'get_pos': {}}
    
  def save(self):
    save = zipfile.ZipFile(main.args[1])
    files = {i:save.open(i).read() for i in save.namelist()}
    files["exits"] = json.dumps({str(list(k)): v for (k,v) in self.exits.iteritems()})
    files["collision"] = json.dumps(self.collision)
    files["entities"] = json.dumps([(entity.__class__.__name__, entity.pos, entity.script) for entity in self.entities])
    save.close()
    save = zipfile.ZipFile(main.args[1], "w", zipfile.ZIP_DEFLATED)
    for f in files:
      save.writestr(f, files[f])
    save.close()
  
  def get_pos(self, x, y, extra=0, view_offset=(0,0)):
    h = hash((x,y,view_offset[0],view_offset[1]))
    if h in self.hash_dict['get_pos']:
      return self.hash_dict['get_pos'][h]
    rtn = ((x-1)*16+view_offset[0]+extra, (y-1)*16+view_offset[1])
    self.hash_dict['get_pos'][h] = rtn
    return rtn
    
  def load_map(self, map_f):
    self.reload_hashes()
    self.map = zipfile.ZipFile(map_f, "r")
    self.map_name = map_f.split("/")[-1]
    namelist = self.map.namelist()
    self.no_layers = len(filter(lambda x: x[:8]=='position', namelist))
    assert(self.no_layers in [1,2])
    self.layers = {"position": [json.load(self.map.open("position"))],\
      "tilesheet": [pygame.image.load(StringIO.StringIO(self.map.read("tilesheet")), ".tga")]}
    if self.no_layers > 1:
      for i in range(self.no_layers-1):
	self.layers["position"].append(json.load(self.map.open("position_%i"%(i+1))))
	self.layers["tilesheet"].append(pygame.image.load(StringIO.StringIO(self.map.read("tilesheet_%i"%(i+1))), ".tga"))
    if 'collision' in namelist:
      self.collision = json.load(self.map.open("collision"))
    else:
      self.collision = self.get_2darray(len(self.layers["position"][0][0]), len(self.layers["position"][0]))
    self.exits = {}
    if 'exits' in namelist:
      exits = json.load(self.map.open("exits"))
      for key in exits:
       self.exits[tuple(json.loads(key))] = exits[key]
    if 'entities' in namelist:
      self.entities = [main.entities[entity[0].lower()](self, entity[1], entity[2]) for entity in json.load(self.map.open("entities"))]
    else:
      self.entities = []
    self.script = json.load(self.map.open("script"))
    self.map.close()
    self.tile_size = self.layers["tilesheet"][0].get_height()
    self.tile_ims = []
    for layer in range(self.no_layers):
      self.tile_ims.append([])
      for tile in range(self.layers["tilesheet"][layer].get_width()//self.tile_size):
	self.tile_ims[-1].append(pygame.Surface((self.tile_size, self.tile_size)))
	if layer != 0:
	  self.tile_ims[-1][-1].set_colorkey((255,255,255))
	self.tile_ims[-1][-1].blit(self.layers["tilesheet"][layer], (0,0), (tile*self.tile_size,0,(tile+1)*self.tile_size,16))
    
    self.tiles = [[[self.tile_ims[layer][self.layers["position"][layer][x][y]] \
      for y in range(len(self.layers["position"][layer][0]))] \
      for x in range(len(self.layers["position"][layer]))] \
      for layer in range(self.no_layers)]
    self.blit_tiles = [i//self.tile_size+1 for i in self.screen.get_size()]
    self.size = [len(self.layers["position"][0]),len(self.layers["position"][0][0])]

  def get_2darray(self, x, y, fill='0'):
    return [[int(fill) \
	for a in range(x)] \
	for b in range(y)]
  
  def get_offset(self):
    return [self.tile_offset[i]+self.blit_tiles[i]/2-1 for i in range(2)] 

  def check_exits(self, d, a):
    offset = self.get_offset()
    for i in [0,a]:
      cur_offset = offset
      cur_offset[d]+=i
      cur_offset = tuple(cur_offset)
      if cur_offset in self.exits:
	e = self.exits[cur_offset]
	if e[3]-1-e[3]%2!=a and e[3]%2==d:
	  return e
  
  def use_exit(self, exit):
    if exit == None: return
    filter_list = [exit[2], self.map_name, exit[0]]
    self.load_map('Assets/Map/Tiles/'+exit[1])
    offset = sorted([k for (k,v) in self.exits.iteritems() if filter_list == v[:3]])
    offset = offset[len(offset)/2]
    self.tile_offset = [offset[0]-self.blit_tiles[0]/2+1,offset[1]-self.blit_tiles[1]/2+1]
    self.view_offset = [8,8]
    d = (self.exits[offset][3]-1)%2
    a = self.exits[offset][3]-2+d
    if a==3:a=-1
    self.tile_offset[d^1]+=a
    self.current_direction=[0,0]
    self.screen.blit_all()
    
  def move(self, d, a):
    if self.current_direction == [0,0]:
      self.current_direction[d]=-2*a
      if len({(self.view_offset[d], self.current_direction[d]), (0,-2), (16,2)})==2:
	self.tile_offset[d]+=a
	self.view_offset[d]^=16
      self.use_exit(self.check_exits(d, a))
      self.screen.blit_all()
    elif self.current_direction == [0,0]:
      self.use_exit(self.check_exits(d, a))
   
  def tick(self):
    if self.current_direction != [0,0]:
      d = int(self.current_direction[1]!=0)
      self.view_offset[d]+=self.current_direction[d]
      if len({(self.view_offset[d], self.current_direction[d]), (0,-2), (16,2)})==2:
	self.tile_offset[d]-=self.current_direction[d]/2
	self.view_offset[d]^=16
      if self.view_offset[d]==8:
	self.current_direction = [0,0]
      self.screen.blit_all()
   
  def draw(self):
    self.player_pos = [self.screen.get_width()/2-16, self.screen.get_height()/2-24]
    self.blit_x = self.tile_offset[0]
    self.blit_y = self.tile_offset[1]
    self.view_x = self.view_offset[0]
    self.view_y = self.view_offset[1]
    
    if self.tile_offset[0] < 0:
      self.blit_x = -1
      self.view_x = -17
      self.player_pos[0] += self.tile_offset[0]*16-self.view_offset[0]+16
    elif self.tile_offset[0]+self.blit_tiles[0]-1 >= self.size[0]:
      self.blit_x = len(self.tiles[0])-self.blit_tiles[0]
      self.view_x = 0
      self.player_pos[0] -= (len(self.tiles[0])-self.blit_tiles[0]-self.tile_offset[0])*16+self.view_offset[0]
    if self.tile_offset[1] < 0:
      self.blit_y = -1
      self.view_y = -17
      self.player_pos[1] += self.tile_offset[1]*16-self.view_offset[1]+16
    elif self.tile_offset[1]+self.blit_tiles[1]-1 >= self.size[1]:
      self.blit_y = len(self.tiles[0][0])-self.blit_tiles[1]
      self.view_y = 0
      self.player_pos[1] -= (len(self.tiles[0][0])-self.blit_tiles[1]-self.tile_offset[1])*16+self.view_offset[1]
  
  def draw_layer(self, layer):
    for x in self.blit_range[0]:
      for y in self.blit_range[1]:
	self.screen.blit_func(self.tiles[layer][self.blit_x+x][self.blit_y+y], self.pos[self.view_x][self.view_y][x][y])
      
    