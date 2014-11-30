from Assets.Map.map import Map
  
class MapView():
  def __init__(self, main, pygame):
    globals()["main"] = main
    globals()["pygame"] = pygame
    self.noclip = 'noclip' in main.args
    self.screen = main.screen
    self.map_f = main.args[1]
    self.map = Map(main, pygame, self.map_f)
    self.coll_surf = pygame.Surface((16,24), pygame.SRCALPHA)
    self.coll_surf.fill((0,128,0,128))    
    self.move_directions = {pygame.K_LEFT: (0,-1),
			    pygame.K_RIGHT:(0, 1),
			    pygame.K_UP:   (1,-1),
			    pygame.K_DOWN: (1, 1)}

  def collide(self, d, a):
    if self.noclip: return True
    offset = self.map.get_offset()
    offset[d]+=a
    if self.map.collision[offset[0]][offset[1]]:
      return False
    for entity in self.map.entities:
      if offset == entity.pos:
	entity.interact(self.map.tile_offset)
	if entity.collideable:
	  return False
    return True

  def run(self, events):
    for event in events:
      if event.type == main.tick_event:
	self.map.tick()
	for e in self.map.entities: e.tick()
      if event.type == pygame.KEYDOWN:
        if event.key in self.move_directions and self.collide(*self.move_directions[event.key]):
	  self.map.move(*self.move_directions[event.key])
    self.map.draw()
    for layer in range(self.map.no_layers):
      self.map.draw_layer(layer)
      if layer == 0:
	for e in self.map.entities: e.draw()
	self.screen.blit_func(self.coll_surf, self.map.player_pos)
    
def add_globals(main, pygame):
  globals()["main"] = main
  globals()["pygame"] = pygame