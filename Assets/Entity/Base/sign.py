import pygame
from Assets.Entity.Base.entity import Entity

class Sign(Entity):
  def interact(self, player_pos):
    if player_pos == [0,-1]:
       self.main.message_box(self.map.script["text"][self.script])

  def draw(self): pass
