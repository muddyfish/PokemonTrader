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

    def run(self, events):
        self.timer = pygame.time.get_ticks()
        if True in [event.type==pygame.KEYDOWN for event in events] and self.timer > 1000:
            main.set_controller("message", "No save file has been detected.", bg = (136,144,248))
        if self.timer > 1720:
            main.screen.blit(self.opening, (0, 0))
            self.stripes.set_alpha(abs(256-(self.timer%4096)/8))
            main.screen.blit(self.stripes, (0, 0))
            main.screen.blit(self.logo, (0, 0))
            if self.timer%500>250: main.screen.blit(self.press_start, (0, 0))
        if self.timer <= 3000:
            self.copyright.set_alpha((3000-self.timer)/5)
            main.screen.blit(self.copyright, (0, 0))
