import pygame

""" Lớp viên đạn """ 
class Bullet:
    def __init__(self, image, x, y):
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.state = 'ready'

    def reset(self):
        self.rect.x = -100  
        self.state = 'ready'
