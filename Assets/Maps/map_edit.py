import zipfile
import json
from Assets.Utility.button import *
from Assets.Utility.entry import *
import map_view
try:
  import cStringIO as StringIO
except ImportError:
  import StringIO
  
class Map(map_view.Map):
  def __init__(self, main, pygame):
    globals()["main"] = main
    globals()["pygame"] = pygame
    map_view.add_globals(main, pygame)
    self.screen = main.screen
    self.map_f = main.args[1]
    self.load_map(self.map_f)
    self.size = main.size
    main.screen=type(main.screen)(pygame.display.set_mode((main.size[0]+100, main.size[1]+200)))
    self.screen = main.screen
    self.tile_offset = [-1,-1]
    self.coll_surf = pygame.Surface((8,8), pygame.SRCALPHA)
    self.coll_surf.fill((128,0,0,128))
    self.button_text = ["Collision", "Exits", "Entities", "Options", "Water"]
    self.buttons = []
    for b in range(len(self.button_text)):
      self.buttons.append(Button(main.size[0]+10, 9+48*b, 80, 32, self.button_text[b], (128,128,0), (0,0,128)))
      self.buttons[-1].draw(self.screen)
    self.subscreen_events = [self.collision_events, self.exit_events, str, str, str]
    self.subscreen_blits =  [self.collision_blits, self.exit_blits, range, range, range]
    self.subscreen = 0
    
    self.exit_entry_name = Input(x=16, y=main.size[1]+16, font = main.entry_font, color=(255,255,255), prompt = "Entrance Name: ")
    self.exit_exit_number = Input(x=16, y=main.size[1]+48, font = main.entry_font, color=(255,255,255), prompt = "Exit Number: ", restricted = '1234567890')
    self.exit_entrance_entry = Input(x=16, y=main.size[1]+80, font = main.entry_font, color=(255,255,255), prompt = "Entrance Number: ", restricted = '1234567890')
    self.exit_entrance_dir = Input(x=16, y=main.size[1]+112, font = main.entry_font, color=(255,255,255), prompt = "Entrance Direction: ", restricted = 'nesw')
    self.nesw = {'':1,"n":1,"e":2,"s":3,"w":4}
    self.nesw_undo = [None,"n","e","s","w"]
    self.xy = [0,1]
    
  def indexes(self, iterable, value):
    indexes = []
    for x, x_val in enumerate(iterable):
      for y, y_val in enumerate(x_val):
	if y_val == value:
	  indexes.append((x,y))
    return indexes
  
  def save(self):
    m = zipfile.ZipFile(self.map_f, "w", zipfile.ZIP_DEFLATED)
    m.writestr("collision", json.dumps(self.collision))
    m.writestr("position", json.dumps(self.position))
    exits = {str(list(k)): v for (k,v) in self.exits.iteritems()}
    m.writestr("exits", json.dumps(exits))
    image = StringIO.StringIO()
    pygame.image.save(self.tilesheet, image)
    m.writestr("tilesheet", image.getvalue())
    
  def collision_events(self, events):
    for event in events:
      if event.type == pygame.MOUSEBUTTONDOWN:
	if event.pos[0] < main.size[0] and event.pos[1] < main.size[1]:
	  x = event.pos[0]/16+self.tile_offset[0]+1
	  y = event.pos[1]/16+self.tile_offset[1]+1
	  x2 = (event.pos[0]/8)%2
	  y2 = (event.pos[1]/8)%2
	  self.screen.blit_all()
	  if event.button == 3:
	    self.collision[x*2+x2][y*2+y2]^=1
	  else:
	    for x,y in self.indexes(self.position, self.position[x][y]):
	      self.collision[x*2+x2][y*2+y2]^=1	      
  def collision_blits(self, x, y):
    pos = self.get_pos(x,y,(16,16),8)
    for x2 in self.xy:
      for y2 in self.xy:
	pos2 = [pos[0]+x2*8, pos[1]+y2*8]
	if self.collision[(x+self.tile_offset[0])*2+x2][(y+self.tile_offset[1])*2+y2]:
	  self.screen.blit_func(self.coll_surf, pos2)
  
  def exit_events(self, events):
    self.exit_entry_name.update(events)
    self.exit_entrance_entry.update(events)
    self.exit_exit_number.update(events)
    self.exit_entrance_dir.update(events)
    for event in events:
      if event.type == pygame.MOUSEBUTTONDOWN:
	if event.pos[0] < main.size[0] and event.pos[1] < main.size[1]:
	  x = event.pos[0]/16+self.tile_offset[0]+1
	  y = event.pos[1]/16+self.tile_offset[1]+1
	  x2 = (event.pos[0]/8)%2
	  y2 = (event.pos[1]/8)%2
	  self.screen.blit_all()
	  key, val = (x*2+x2,y*2+y2), (int(self.exit_exit_number), self.exit_entry_name.value, int(self.exit_entrance_entry), self.nesw[self.exit_entrance_dir.value])
	  if key in self.exits:
	    if event.button == 3:
	      self.exit_exit_number.value = str(self.exits[key][0])
	      self.exit_exit_number.blit = True
	      self.exit_entry_name.value = self.exits[key][1]
	      self.exit_entry_name.blit = True
	      self.exit_entrance_entry.value = str(self.exits[key][2])
	      self.exit_entrance_entry.blit = True
	      self.exit_entrance_dir.value = self.nesw_undo[self.exits[key][3]]
	      self.exit_entrance_dir.blit = True
	    else:
	      del self.exits[key]
	  else:
	    self.exits[key] = val
	  self.screen.blit_rects.append(((8*x, 8*y, 8,8)))
  def exit_blits(self, x, y):
    self.exit_entry_name.draw(self.screen)
    self.exit_entrance_entry.draw(self.screen)
    self.exit_exit_number.draw(self.screen)
    self.exit_entrance_dir.draw(self.screen)
    pos = self.get_pos(x,y,(16,16),8)
    for x2 in self.xy:
      for y2 in self.xy:
	pos2 = [pos[0]+x2*8, pos[1]+y2*8]
	if ((x+self.tile_offset[0])*2+x2, (y+self.tile_offset[1])*2+y2) in self.exits:
	  self.screen.blit_func(self.coll_surf, pos2)
  
  def run(self, events):
    for event in events:
      if event.type == pygame.KEYDOWN:
	if event.key == pygame.K_LEFT: self.tile_offset[0]-=1
	if event.key == pygame.K_RIGHT:self.tile_offset[0]+=1
	if event.key == pygame.K_UP:   self.tile_offset[1]-=1
	if event.key == pygame.K_DOWN: self.tile_offset[1]+=1
	if event.key == pygame.K_TAB: self.save()
	self.screen.blit_all()
      if event.type == pygame.MOUSEBUTTONDOWN:
        if event.pos[0] > main.size[0]:
	  for b in range(len(self.buttons)):
	    if self.buttons[b].pressed(event.pos):
	      self.subscreen = b
	      self.screen.fill((0,0,0))
	      for button in self.buttons:
		button.draw(self.screen)
	      self.screen.blit_all()
    self.subscreen_events[self.subscreen](events)
    for x in xrange(self.blit_tiles[0]):
      for y in xrange(self.blit_tiles[1]):
	pos = self.get_pos(x,y, (0,0))
	try:
	  self.screen.blit_func(self.tiles[x+self.tile_offset[0]][y+self.tile_offset[1]], pos)
	  self.subscreen_blits[self.subscreen](x, y)
	except IndexError: pass