def twodrange(x, y):
  for i in range(x):
    for j in range(y):
      yield (i, j)

class Message():
  def __init__(self, main, pygame, returnobj, message):
    globals()["pygame"] = pygame
    globals()["main"] = main
    
    self.return_obj = returnobj
    self.message = message
    self.screen = main.screen
    
    self.skin_id = 0
    self.start_time = pygame.time.get_ticks()
    self.speed = 1
    self.speed*=50
    
    self.message_boxes = main.asset_loader.load_image("Message/boxes.png")
    self.xy = (self.message_boxes.get_width()/30, self.message_boxes.get_height()/30)
    self.skins = [self.piece_skin(self.convert_skin(skin, (3,3), 8, 1)) \
       for skin in self.convert_skin(self.message_boxes, self.xy, 27, 3)]
    self.pos = (16, self.screen.get_height()-self.skins[0].get_height()-16)
    self.text_pos = [(24, self.pos[1]+i) for i in [8, 24]]

    self.txt = [self.render_text(msg[1]) for msg in self.message]
    self.text_line = 0

  def convert_skin(self, orig, size, cropped, inc):
    inc += cropped
    skins = []
    for x, y in twodrange(*size):
      skin = pygame.Surface((cropped,cropped))
      skin.set_colorkey((255,255,0))
      skin.blit(orig, (0,0), (x*inc,y*inc,(x+1)*inc,(y+1)*inc))
      skins.append(skin)
    return skins    
  
  def piece_skin(self, orig):
    sx = 35
    sy = 5
    skin = pygame.Surface(((sx+1)*8,(sy+1)*8))
    placement = {(0 ,0): 0, (0 ,-1): 1, (0 ,sy): 2,\
		 (-1,0): 3, (-1,-1): 4, (-1,sy): 5,\
		 (sx,0): 6, (sx,-1): 7, (sx,sy): 8}
    for xy in twodrange(sx+1, sy+1):
      piece = placement[(-1,-1)]
      if xy in placement:
	piece = placement[xy]
      else:
	for i in [0,1]:
	  nxy = list(xy)
	  nxy[i] = -1
	  nxy = tuple(nxy)
	  if nxy in placement:
	    piece = placement[nxy]
      skin.blit(orig[piece], (xy[0]*8, xy[1]*8))
    return skin
  
  def render_text(self, text):
    return [main.message_font.render(text[:i], False, (0,0,0)) for i in range(len(text)+1)]
  
  def leave(self):
    self.screen.blit_rects.append(((0,0), self.screen.get_size()))
    main.screen_control = self.return_obj
    main.screen_control_name = self.return_obj.__class__.__name__
  
  def run(self, events):
    self.timer = pygame.time.get_ticks()-self.start_time
    if self.text_line == len(self.txt):
      if 1000-self.timer < 0: self.leave()
    else:
      self.screen.blit(self.skins[self.skin_id], self.pos)
      offset = self.timer/self.speed
      line_0 = (self.text_line!=0)+0
      if line_0:
	for i in range(self.text_line):
	  offset-=len(self.txt[i])
	self.screen.blit(self.txt[self.text_line-1][-1], self.text_pos[0])
      try:
	self.screen.blit(self.txt[self.text_line][offset], self.text_pos[line_0])
      except IndexError:
	self.screen.blit(self.txt[self.text_line][-1], self.text_pos[line_0])
	self.text_line+=1
	if self.text_line == len(self.txt): self.start_time += self.timer