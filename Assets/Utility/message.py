from itertools import permutations

class InteractionPair(tuple):
    def __new__(cls, a, b):
        if a <= b:
            return tuple.__new__(cls, (a, b))
        return tuple.__new__(cls, (b, a))

class Message():
    def __init__(self, main, pygame, message, position = (9, 113), bg = None, return_to = "logo"):
        #Add the pygame module to the global variable list
        globals()["pygame"] = pygame
        globals()["main"] = main
        self.size = main.settings["size"]
        self.message_speed = main.settings["speed"]
        # If the input message is a string, add the drawn versions
        if isinstance(message, basestring): 
            message = message.split("\n")
            self.message_text = []
            self.messages = []
            for m in message:
                self.message_text.append([])
                self.messages.append([])
                sub = 0
                for i in range(len(m)+1):
                    text = main.font.render(m[sub:i], True, (0,0,0), (248,248,248))
                    self.message_text[-1].append(m[sub:i])
                    if text.get_size()[0] > 196:
                        self.messages.append([])
                        self.message_text.append([])
                        sub = i-1
                    self.messages[-1].append(text)
            self.message_text = [m[-1] for m in self.message_text]
        else: # If not, just take them
            self.message_text, self.messages = message
        self.position = position # Message box position
        self.bg = bg
        if bg == None: #If not given a colour, help everything else that happens to be being blitted.
            self.bg = main.screen.copy()
        self.return_to = return_to # What are you returning to?
        self.speech_box = self.create_msg_box((222,46))
        self.start_time = pygame.time.get_ticks()
        self.max_messages = sum(map(len, self.messages))-1

    def run(self, events):
        self.timer = pygame.time.get_ticks()-self.start_time
        keydown = True in [event.type==pygame.KEYDOWN for event in events]
        if keydown: self.start_time = -1000000
        if isinstance(self.bg, tuple):
            main.screen.fill(self.bg)
        else:
            main.screen.blit(self.bg, (0,0))
        main.screen.blit(self.speech_box, self.position)
        message = min((self.timer*self.message_speed)/1000, self.max_messages)
        if message == -1:
            if self.return_to in main.controllers.keys():
                main.set_controller(self.return_to)
            else:
                main.screen_controller = self.return_to
        elif message >= sum(map(len, self.message_text[:2])) and keydown: 
            main.set_controller("message", [self.message_text[2:], self.messages[2:]], self.position, self.bg, self.return_to)
        else:
            if message > len(self.messages[0]):
                index = min(len(self.messages[1])-1, message-len(self.messages[0])+1)
                main.screen.blit(self.messages[1][index], (self.position[0]+7, self.position[1]+25))
            main.screen.blit(self.messages[0][min(len(self.messages[0])-1, message)], (self.position[0]+7, self.position[1]+9))

    def create_msg_box(self, size):
        surf = pygame.Surface(size)
        surf.set_colorkey((255,255,255))
        surf.fill((248,248,248))
        self.surf_comps = [pygame.image.load("Icons/sb_%s.png"%(i)).convert() for i in range(1,5)]
        self.surf_comps.append(pygame.transform.rotate(self.surf_comps[3], 180))
        self.surf_comps.append(pygame.transform.rotate(self.surf_comps[3], 90))
        for i in range(size[0]):
            surf.blit(self.surf_comps[1], (i,0))
            surf.blit(self.surf_comps[5], (i,size[1]-5))
        for i in range(size[1]):
            surf.blit(self.surf_comps[3], (0,i))
            surf.blit(self.surf_comps[4], (size[0]-5,i))

        surf.blit(self.surf_comps[0], (0,0))
        surf.blit(pygame.transform.flip(self.surf_comps[0], True, False), (size[0]-6,0))
        surf.blit(self.surf_comps[2], (0,size[1]-6))
        surf.blit(pygame.transform.flip(self.surf_comps[2], True, False), (size[0]-6,size[1]-6))
        return surf
