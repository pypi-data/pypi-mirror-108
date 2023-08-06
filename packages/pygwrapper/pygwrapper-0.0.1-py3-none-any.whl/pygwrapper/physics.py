import pygame,pymunk,os
class DummyFrame:
    def __init__(self,x,y,img,screen):
        self.image = pygame.image.load(img)
        self.screen = screen


class PhysicsBody2D(DummyFrame):
    def __init__(self,x,y,img,screen,space,body_type):
        super().__init__(x,y,img,screen)
        self.body = pymunk.Body(1,100,body_type=body_type)
        self.body.position = (x,y)
        self.rect = self.image.get_rect(topleft=(x,y))
        self.body.shape = pymunk.Poly.create_box(self.body, (self.rect.width, self.rect.height))
        space.add(self.body, self.body.shape)
    def show(self):
        self.screen.blit(self.image,(int(self.body.position.x),int(self.body.position.y)))
        self.rect.x,self.rect.y = int(self.body.position.x),int(self.body.position.y)
        pygame.draw.rect(self.screen,(0,0,0),self.rect,1)
