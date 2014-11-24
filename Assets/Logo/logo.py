class Logo():
    def __init__(self, main, pygame):
        globals()["pygame"] = pygame
        globals()["main"] = main
        self.size = main.settings["size"]
        self.copyright = pygame.image.load("Icons/Copyright.png").convert(24)
        self.opening = pygame.image.load("Icons/Emerald_Opening.png").convert()
        self.logo = pygame.image.load("Icons/Logo.png").convert_alpha()
        self.press_start = pygame.image.load("Icons/Press_Start.png").convert_alpha()
        self.stripes = pygame.image.load("Icons/Raquaza_Stripes.png").convert()
        self.stripes.set_colorkey((255,255,255))

        self.speed = main.settings["speed"]
        self.alpha_time = 3000
        self.add_time = 0

    def run(self, events):
        self.timer = pygame.time.get_ticks()+self.add_time
        copyright_alpha = 2*(self.alpha_time-self.timer)/self.speed
        if True in [event.type==pygame.KEYDOWN for event in events]:
            if copyright_alpha > 0:
                self.add_time = self.alpha_time
            else:
                main.debug_message("DEBUG")
        if self.timer >= copyright_alpha-255:
            main.screen.blit(self.opening, (0, 0))
            self.stripes.set_alpha(abs(256-(self.timer%(512*self.speed))/self.speed))
            main.screen.blit(self.stripes, (0, 0))
            main.screen.blit(self.logo, (0, 0))
            if self.timer%(self.speed*100)>self.speed*50:
                main.screen.blit(self.press_start, (0, 0))
        if self.timer <= self.alpha_time:
            self.copyright.set_alpha(copyright_alpha)
            main.screen.blit(self.copyright, (0, 0))
