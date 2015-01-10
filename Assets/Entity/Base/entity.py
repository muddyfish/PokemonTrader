import pygame

class Entity(object):
  def __init__(self, map, pos, script):
    self.map = map
    self.main = self.map.main
    self.screen = map.screen
    self.pos = pos
    self.script = script
    self.view_offset = [0,0]
    self.collideable = True
    self.sprite = pygame.Surface((16,16), pygame.SRCALPHA)
    self.sprite.fill((0,128,128,128))
    self.asset_loader = map.asset_loader
    
  def extra_args(self):
    return []
    
  def draw(self):
    if 0<self.pos[0]-self.map.blit_x<self.map.blit_tiles[0] and \
       0<self.pos[1]-self.map.blit_y<self.map.blit_tiles[1]:
      pos = self.map.pos[self.view_offset[0]+self.map.view_x] \
			[self.view_offset[1]+self.map.view_y] \
			[self.pos[0]-self.map.blit_x] \
			[self.pos[1]-self.map.blit_y]
      self.screen.blit(self.sprite, pos)
  
  def interact(self, player_pos):
    pass
  
  def tick(self):
    pass