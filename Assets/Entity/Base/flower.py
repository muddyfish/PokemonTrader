import pygame, random
from Assets.Entity.Base.entity import Entity

class Flower(Entity):
  def __init__(self, map, pos, script):
    super(Flower, self).__init__(map, pos, script)
    self.collideable = False
    self.spritesheet = self.asset_loader.load_image("Entity/flower.png", True)
    self.sprites = []
    self.tile_size = self.spritesheet.get_height()
    self.no_sprites = self.spritesheet.get_width()//self.tile_size
    for tile in range(self.no_sprites):
      self.sprites.append(pygame.Surface((self.tile_size, self.tile_size), pygame.SRCALPHA))
      self.sprites[-1].blit(self.spritesheet, (0,0), (tile*self.tile_size,0,(tile+1)*self.tile_size,16))
    self.sprites.extend(self.sprites[-2::-1])
    self.no_sprites+=self.no_sprites-1
    self.sprite_no = random.randrange(self.no_sprites)
    self.sprite = self.sprites[0]
    self.tick_no = 0
    
  def tick(self):
    self.tick_no = (self.tick_no+1)%7
    if self.tick_no == 0:
      self.sprite_no = (self.sprite_no+1)%self.no_sprites
      self.sprite = self.sprites[self.sprite_no]