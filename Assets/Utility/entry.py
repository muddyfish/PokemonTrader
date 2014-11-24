from pygame.locals import *
import pygame
import string
import button

class Input:
  """ A text input for pygame apps """
  def __init__(self, font, x=0, y=0, color=(0,0,0), restricted=string.printable, maxlength=-1, prompt="''"):
    """ Options: x, y, font, color, restricted, maxlength, prompt """
    self.x = x
    self.y = y
    self.font = font
    self.color = color
    self.restricted = restricted
    self.maxlength = maxlength
    self.prompt = prompt;
    self.value = ''
    self.shifted = False
    self.focus = False
    self.text_size = self.font.render(self.prompt, 1, self.color).get_size()
    self.button = button.Button(self.x, self.y, *self.text_size)
    self.blit = True
    
  def __str__(self):
    return self.value
  
  def __int__(self):
    if self.value == '': return 0
    return int(self.value)

  def draw(self, surface):
    """ Draw the text input to a surface """
    if self.blit:
      surface.fill((0,0,0), ((self.x, self.y), self.text_size))
      text = self.font.render(self.prompt+self.value, 1, self.color)
      self.text_size = text.get_size()
      self.button.length, self.button.height = self.text_size
      surface.blit(text, (self.x, self.y))
      self.blit = False

  def update(self, events):
    """ Update the input based on passed events """
    for event in events:
      if event.type == MOUSEBUTTONDOWN:
	self.focus = self.button.pressed(event.pos)
      if event.type == KEYUP:
        if event.key == K_LSHIFT or event.key == K_RSHIFT: self.shifted = False
      if event.type == KEYDOWN and self.focus:
        if event.key == K_BACKSPACE: self.value = self.value[:-1]
        if event.unicode != None:
	  if event.key == K_LSHIFT or event.key == K_RSHIFT: self.shifted = True
	  elif event.key == K_SPACE: self.value += ' '
	  keyname = pygame.key.name(event.key)
	  if len(keyname)==1:
	    if self.shifted: keyname = keyname.upper()
	    if keyname in self.restricted: self.value+= keyname
	self.blit = True

    if len(self.value) > self.maxlength and self.maxlength >= 0: self.value = self.value[:-1]
