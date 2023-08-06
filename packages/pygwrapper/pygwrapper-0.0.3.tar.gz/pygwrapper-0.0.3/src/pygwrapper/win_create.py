import pygame
import pymunk
pygame.init()

def nothing():
    pass
class GameInstance:
    def __init__(self,width,height):
        self.win = pygame.display.set_mode((width,height))
        self.clock = pygame.time.Clock()
        self.space = pymunk.Space()

    def start_window(self,caption,mainloop,get_event=nothing,on_quit=nothing):
        pygame.display.set_caption(caption)
        self.space.gravity = (0,500)
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    on_quit()
                get_event()
            mainloop()
            pygame.display.update()
            self.clock.tick(120)
            self.space.step(1/120)
        pygame.quit()
