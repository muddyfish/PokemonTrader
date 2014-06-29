from dummy import *
import pygame, glob, json, os

class Main:  
    def __init__(self):
        #Init pygame
        pygame.init()
        self.load_settings()
        if self.settings["fullscreen"]: self.full = pygame.FULLSCREEN
        else: self.full = 0
        #Create the display
        self.screen = pygame.display.set_mode(tuple(self.settings["size"]), self.full) 
        pygame.display.set_caption("Pokemon")
        self.clock=pygame.time.Clock()
        self.screen_controller = Dummy()

    def run(self):
        while 1:
            self.clock.tick()
            events = pygame.event.get()
            for event in events: #Events that are always done
                if event.type == pygame.QUIT: self.exit()
                elif event.type == pygame.KEYDOWN: 
                    if event.key == pygame.K_BACKSPACE: self.screenshot()
                    if event.key == pygame.K_ESCAPE: self.exit()
            self.screen_controller.run(events) #Other events
            fps = self.fps_font.render("Frames Calculated: %d"%(self.clock.get_fps()) , True, (255,255,255))
            self.screen.blit(fps, (10, 10))
            pygame.display.flip()

    def screenshot(self):
        print("Screenshot")
        screenshots = [int(screenshot[25:-4]) for screenshot in glob.glob("./Screenshots/screenshot_*.png")]
        if screenshots == []: screenshot_num = 1
        else: screenshot_num = max(screenshots)
        pygame.image.save(self.screen, "Screenshots/screenshot_%s.png" %(screenshot_num))

    def exit(self):
        pygame.quit()
        sys.exit()

    def load_settings(self):
        file_obj = open("settings.json")
        self.settings = json.load(file_obj)
        file_obj.close()

    def save_settings(self, data):
        file_obj = open("settings.json", "w")
        self.settings = json.dump(file_obj)
        file_obj.close()

def main():
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    main = Main()
    main.run()

if __name__ == "__main__":
    main()


