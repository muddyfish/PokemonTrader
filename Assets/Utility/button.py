import pygame

class Button():
  def __init__(self, x, y, length, height, text='', text_color=(0,0,0), color=(255,255,255)):
    self.x, self.y, self.length, self.height, self.text, self.text_color, self.color = x, y, length, height, text, text_color, color
    
  def draw(self, surface):
    surface = self.draw_button(surface)
    surface = self.write_text(surface)

  def write_text(self, surface):
    myFont = pygame.font.SysFont("velvenda", 18)
    myText = myFont.render(self.text, 1, self.text_color)
    surface.blit(myText, ((self.x+self.length/2) - myText.get_width()/2, (self.y+self.height/2) - myText.get_height()/2))
    return surface

  def draw_button(self, surface):       
    for i in range(1,10):
      s = pygame.Surface((self.length+(i*2),self.height+(i*2)))
      s.fill(self.color)
      alpha = (255/(i+2))
      if alpha <= 0:
        alpha = 1
      s.set_alpha(alpha)
      surface.blit(s, (self.x-i,self.y-i))
    return surface

  def pressed(self, mouse):
    if mouse[0] > self.x:
      if mouse[1] > self.y:
        if mouse[0] < self.x+self.length:
          if mouse[1] < self.y+self.height:
            return True
          else: return False
        else: return False
      else: return False
    else: return False
 
