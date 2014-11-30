import zipfile
import json
from Assets.Utility.button import *
from Assets.Utility.entry import *
from Assets.Map.map import Map
try:
  import cStringIO as StringIO
except ImportError:
  import StringIO
  
class MapEdit(object):
  def __init__(self, main, pygame):
    globals()["main"] = main
    globals()["pygame"] = pygame
    self.screen = main.screen
    self.map = Map(main, pygame, main.args[1])
    #Make map not spill out
    self.map.blit_tiles = [i//self.map.tile_size for i in self.screen.get_size()]
    self.map.blit_range = [range(self.map.blit_tiles[i]) for i in [0,1]]
    #Resize the screen
    self.size = main.size
    main.screen=type(main.screen)(pygame.display.set_mode((main.size[0]+100, main.size[1]+200)))
    self.screen = main.screen
    #Red surf
    self.coll_surf = pygame.Surface((16,16), pygame.SRCALPHA)
    self.coll_surf.fill((128,0,0,128))    
    #Setup Subscreens
    self.collision_setup()
    self.exit_setup()
    self.entity_setup()
    self.button_text = ["Collision", "Exits", "Entities", "Options", "Water"]
    self.buttons = []
    for b in range(len(self.button_text)):
      self.buttons.append(Button(main.size[0]+10, 9+48*b, 80, 32, self.button_text[b], (128,128,0), (0,0,128)))
      self.buttons[-1].draw(self.screen)
    self.subscreen_events = [self.collision_events, self.exit_events, self.entity_events, str, str]
    self.subscreen_blits =  [self.collision_blits, self.exit_blits, self.entity_blits, xrange, xrange]
    self.subscreen = 0
    self.xy = [0,1]
    
  def indexes(self, iterable, value):
    indexes = []
    for x, x_val in enumerate(iterable):
      for y, y_val in enumerate(x_val):
	if y_val == value:
	  indexes.append((x,y))
    return indexes
  
  def get_pos_from_mouse(self, event):
    return (event.pos[0]/16+self.map.tile_offset[0], (event.pos[1]-8)/16+self.map.tile_offset[1]+1)
  
  def collision_setup(self):
    pass
  def collision_events(self, events):
    for event in events:
      if event.type == pygame.MOUSEBUTTONDOWN:
	if event.pos[0] < main.size[0] and event.pos[1] < main.size[1]:
	  x, y = self.get_pos_from_mouse(event)
	  self.screen.blit_all()
	  if event.button == 3:
	    self.map.collision[x][y]^=1
	  else:
	    for x,y in self.indexes(self.map.layers["position"][0], self.map.layers["position"][0][x][y]):
	      self.map.collision[x][y]^=1	      
  def collision_blits(self, x, y):
    pos = self.get_pos(x,y)
    if self.map.collision[(x+self.map.tile_offset[0])][(y+self.map.tile_offset[1])]:
      self.screen.blit_func(self.coll_surf, pos)
  
  def exit_setup(self):
    self.exit_entry_name = Input(x=16, y=main.size[1]+16, font = main.entry_font, color=(255,255,255), prompt = "Entrance Name: ")
    self.exit_exit_number = Input(x=16, y=main.size[1]+48, font = main.entry_font, color=(255,255,255), prompt = "Exit Number: ", restricted = '1234567890')
    self.exit_entrance_entry = Input(x=16, y=main.size[1]+80, font = main.entry_font, color=(255,255,255), prompt = "Entrance Number: ", restricted = '1234567890')
    self.exit_entrance_dir = Input(x=16, y=main.size[1]+112, font = main.entry_font, color=(255,255,255), prompt = "Entrance Direction: ", restricted = 'nesw')
    self.nesw = {'':1,"n":1,"e":2,"s":3,"w":4}
    self.nesw_undo = [None,"n","e","s","w"]
  def exit_events(self, events):
    self.exit_entry_name.update(events)
    self.exit_entrance_entry.update(events)
    self.exit_exit_number.update(events)
    self.exit_entrance_dir.update(events)
    for event in events:
      if event.type == pygame.MOUSEBUTTONDOWN:
	if event.pos[0] < main.size[0] and event.pos[1] < main.size[1]:
	  x, y = self.get_pos_from_mouse(event)
	  self.screen.blit_all()
	  key, val = (x,y), (int(self.exit_exit_number), self.exit_entry_name.value, int(self.exit_entrance_entry), self.nesw[self.exit_entrance_dir.value])
	  if key in self.map.exits:
	    if event.button == 3:
	      self.exit_exit_number.value = str(self.map.exits[key][0])
	      self.exit_exit_number.blit = True
	      self.exit_entry_name.value = self.map.exits[key][1]
	      self.exit_entry_name.blit = True
	      self.exit_entrance_entry.value = str(self.map.exits[key][2])
	      self.exit_entrance_entry.blit = True
	      self.exit_entrance_dir.value = self.nesw_undo[self.map.exits[key][3]]
	      self.exit_entrance_dir.blit = True
	    else:
	      del self.map.exits[key]
	  else:
	    self.map.exits[key] = val
	  self.screen.blit_rects.append(((16*x, 16*y, 16,16)))
  def exit_blits(self, x, y):
    self.exit_entry_name.draw(self.screen)
    self.exit_entrance_entry.draw(self.screen)
    self.exit_exit_number.draw(self.screen)
    self.exit_entrance_dir.draw(self.screen)
    pos = self.get_pos(x,y)
    if (x+self.map.tile_offset[0], y+self.map.tile_offset[1]) in self.map.exits:
      self.screen.blit_func(self.coll_surf, pos)
      
  def entity_setup(self):
    self.entity_selected = None
    self.all_entities = [entity(self.map, (0,0)) for entity in main.entities.values()]
  def entity_events(self, events):
    for event in events:
      if event.type == pygame.MOUSEBUTTONDOWN:
	if event.pos[0]%32>=16 and 0<event.pos[1]-main.size[1]-16<=16:
	  self.entity_selected = event.pos[0]/32
	  self.screen.blit_all()
	elif event.pos[0] < main.size[0] and event.pos[1] < main.size[1] and self.entity_selected!=None:
	  x, y = self.get_pos_from_mouse(event)
	  self.screen.blit_all()
	  entity_class = self.all_entities[self.entity_selected].__class__
	  sametype = False
	  for i, entity in enumerate(self.map.entities):
	    if entity.pos == (x,y):
	      if entity.__class__ == entity_class:
		sametype = True
	      del self.map.entities[i]
	      break
	  if not sametype:
	    self.map.entities.append(entity_class(self.map, (x,y)))
  def entity_blits(self, x, y):
    for i, entity in enumerate(self.all_entities):
      self.screen.blit_func(entity.sprite, (32*i+16,main.size[1]+16))
      if self.entity_selected == i:
	self.screen.blit_func(self.coll_surf, (32*i+16,main.size[1]+16))
    for entity in self.map.entities:
      entity.draw()
  
  def get_pos(self, x,y):
    return self.map.pos[self.map.view_x] \
		       [self.map.view_y] \
		       [(x+self.map.tile_offset[0])-self.map.blit_x] \
		       [(y+self.map.tile_offset[1])-self.map.blit_y]
  
  def run(self, events):
    for event in events:
      if event.type == pygame.KEYDOWN:
	if event.key == pygame.K_LEFT: self.map.tile_offset[0]-=1
	if event.key == pygame.K_RIGHT:self.map.tile_offset[0]+=1
	if event.key == pygame.K_UP:   self.map.tile_offset[1]-=1
	if event.key == pygame.K_DOWN: self.map.tile_offset[1]+=1
	self.map.tile_offset[0]=max(0,self.map.tile_offset[0])
	self.map.tile_offset[1]=max(0,self.map.tile_offset[1])
	self.map.tile_offset[0]=min(self.map.size[0]-self.map.blit_tiles[0],self.map.tile_offset[0])
	self.map.tile_offset[1]=min(self.map.size[1]-self.map.blit_tiles[1],self.map.tile_offset[1])
	if event.key == pygame.K_TAB: self.map.save()
	self.screen.blit_all()
      if event.type == pygame.MOUSEBUTTONDOWN:
        if event.pos[0] > main.size[0]:
	  for b in range(len(self.buttons)):
	    if self.buttons[b].pressed(event.pos):
	      self.subscreen = b
	      self.screen.fill((0,0,0))
	      for button in self.buttons:
		button.draw(self.screen)
	      self.exit_entry_name.blit = True
	      self.exit_entrance_entry.blit = True
	      self.exit_exit_number.blit = True
	      self.exit_entrance_dir.blit = True
	      self.screen.blit_all()
    self.subscreen_events[self.subscreen](events)
    self.map.draw()
    self.map.draw_layer(0)
    for x in xrange(self.map.blit_tiles[0]):
      for y in xrange(self.map.blit_tiles[1]):
	pos = self.map.get_pos(x,y)
	try:
	  self.subscreen_blits[self.subscreen](x, y)
	except IndexError: pass