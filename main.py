#Import modules
import pygame
import sys
import glob
import os
import json
import inspect

import Assets.Utility.asset_loader as asset_loader
import Assets.Maps.map_edit as map_edit
import Assets.Maps.map_view as map_view

class Main:
  def __init__(self):
    self.load_settings()
    self.size = (320,240)
    self.fullscreen = 0
    if self.settings["fullscreen"]:
      self.fullscreen = pygame.FULLSCREEN
    self.fps_limit = self.settings["fps_limit"]
    
    #Init pygame
    pygame.init()
    self.screen = Screen(pygame.display.set_mode(tuple(self.size), self.fullscreen)) #Create the display
    pygame.display.set_caption("ALTTP")
    self.clock = pygame.time.Clock()
    self.key_event = pygame.USEREVENT+1
    self.key_speed = 100
    self.tick_event = pygame.USEREVENT+2
    self.tick_speed = 25
    pygame.time.set_timer(self.key_event, self.key_speed)
    pygame.time.set_timer(self.tick_event, self.tick_speed)
    self.args = sys.argv

    self.entry_font=pygame.font.SysFont("vervanda", 18)
    self.fps_font=pygame.font.SysFont("vervanda", 12)

    self.asset_loader = asset_loader.AssetLoader(pygame)
    self.controllers = {
      "map_edit": map_edit.Map,
      "map_view": map_view.Map}
    self.screen_control = None
    cont = 'map_view'
    if 'edit' in self.args:
      cont = 'map_edit'
    self.change_controller(cont)
    self.screen.blit_all()
    
  def run(self):
    while 1:
      self.clock.tick(self.fps_limit)
      events = pygame.event.get()
      for event in events: #Events that are always done
	if event.type == self.key_event:
	  keys = pygame.key.get_pressed()
	  for key in xrange(len(keys)):
	    if keys[key]:
	      e = pygame.event.Event(pygame.KEYDOWN, {"unicode": None, "key": key, "mod": pygame.key.get_mods()})
	      events.append(e)
        if event.type == pygame.QUIT: self.quit()
        if event.type == pygame.KEYDOWN: 
          if event.key == 167 and event.unicode != None: self.screenshot()
          elif event.key == pygame.K_ESCAPE:  self.quit()
         
      self.screen_control.run(events) #Other events
      fps = self.fps_font.render("FPS: %d" %(int(self.clock.get_fps())), True, (255,255,255))
      self.screen.blit(fps, (10, 30))
      pygame.display.update(self.screen.blit_rects_old)
      pygame.display.update(self.screen.blit_rects)
      self.screen.blit_rects_old = self.screen.blit_rects
      self.screen.blit_rects = []
      
  def screenshot(self):
    print("Screenshot")
    globs = glob.glob("./Screenshots/screenshot_*.png")
    latest_num=0
    if len(globs) != 0: latest_num = max([int(f.split("_")[-1][:-4]) for f in globs])
    pygame.image.save(self.screen.copy(), "Screenshots%sscreenshot_%i.png" %(os.sep, latest_num+1))

  def change_controller(self,new):
    self.screen.blit_rects.append(((0,0), self.screen.get_size()))
    self.screen_control_name=new
    self.screen_control=self.controllers[self.screen_control_name](self, pygame)
      
  def quit(self):
    pygame.quit()
    sys.exit()

  def load_settings(self):
    file_obj = open("settings.json")
    self.settings = json.load(file_obj)
    file_obj.close()

  def save_settings(self):
    file_obj = open("settings.json", "w")
    json.dump(file_obj, self.settings)
    file_obj.close()

class Screen(object):
  def __init__(self, surf):
    self.blit_rects = []
    self.blit_rects_old = []
    for name, val in inspect.getmembers(surf):
      if name != "blit":
        try: setattr(self, name, val)
        except TypeError: pass
      else:
        self.blit_func = val
    self.size = self.get_size()
    
  def blit(self, *args, **kargs):
    self.blit_rects.append(self.blit_func(*args, **kargs))
    
  def blit_all(self):
    self.blit_rects=[((0,0), self.size)]
    
def main():
  os.environ['SDL_VIDEO_CENTERED'] = '1'
  Main().run()

if __name__ == "__main__":
  if "debug" in sys.argv:
    try: import cProfile as profile
    except ImportError: import profile
    profile.run('main()')
  else:
    main()
