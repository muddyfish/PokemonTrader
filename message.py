class Message():
    def __init__(self, main, pygame, message, position = (9, 113), bg = None):
        globals()["pygame"] = pygame
        globals()["main"] = main
        self.size = main.settings["size"]
        self.message_speed = main.settings["speed"]
        self.message = message
        self.position = position
        self.bg = bg
        self.speech_box = pygame.image.load("Icons/Speech_Box.png").convert_alpha()
        self.start_time = pygame.time.get_ticks()
        self.messages = []
        for i in range(len(message)+1):
            self.messages.append(main.font.render(message[:i], True, (0,0,0)))

    def run(self, events):
        self.timer = pygame.time.get_ticks()-self.start_time
        if True in [event.type==pygame.KEYDOWN for event in events]:
            main.set_controller("message", "No save file has been detected.")
        if self.bg:
            main.screen.fill(self.bg)
        main.screen.blit(self.speech_box, self.position)
        message = self.messages[min((self.timer*self.message_speed)/1000, len(self.messages)-1)]
        main.screen.blit(message, (self.position[0]+7, self.position[1]+9))
