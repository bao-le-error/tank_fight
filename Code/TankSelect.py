import pygame
from pygame.locals import *


GRAPHICS_FOLDER = "Graphics/"
SOUND_FOLDER = "Sounds/"
FONT_FOLDER = "Font/"

class TankSelect:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption('Select Tank')
        self.clock = pygame.time.Clock()
        self.running = True
        self.tanks = [GRAPHICS_FOLDER + '1.png', GRAPHICS_FOLDER + '4.png',GRAPHICS_FOLDER + '6.png',GRAPHICS_FOLDER + '7.png',GRAPHICS_FOLDER + '8.png',GRAPHICS_FOLDER + '11.png',GRAPHICS_FOLDER + '12.png',GRAPHICS_FOLDER + '20.png',GRAPHICS_FOLDER + '21.png',GRAPHICS_FOLDER + '23.png',
                      GRAPHICS_FOLDER + '2.png', GRAPHICS_FOLDER + '3.png',GRAPHICS_FOLDER + '5.png',GRAPHICS_FOLDER + '9.png',GRAPHICS_FOLDER + '10.png',GRAPHICS_FOLDER + '18.png',GRAPHICS_FOLDER + '13.png',GRAPHICS_FOLDER + '14.png',GRAPHICS_FOLDER + '15.png',GRAPHICS_FOLDER + '16.png']
        self.selected_tanks = [None, None]
        self.font = pygame.font.Font(FONT_FOLDER + 'wheaton capitals.ttf', 30)
        self.confirm_button = pygame.Rect(325, 500, 150, 50)
        self.player1_text = self.font.render("Player 1", True, (255, 255, 255))
        self.player2_text = self.font.render("Player 2", True, (255, 255, 255))
        self.tank_select = self.font.render("Tank Select", True, (255, 255, 255))
        self.button_sound = pygame.mixer.Sound(SOUND_FOLDER +'button.mp3')

    def draw_tanks(self):
        tank_width, tank_height = 60, 60
        tank_spacing = 20
        column_spacing = 80
        left_start_x = 100
        right_start_x = 500
        start_y = 110
        border_thickness = 3  
        border_margin = 5    

        self.screen.blit(self.player1_text, (left_start_x + 50, start_y - 40))
        self.screen.blit(self.player2_text, (right_start_x + 50, start_y - 40))
        self.screen.blit(self.tank_select, (300, 10))
        
        for i in range(10):
            left_tank_x = left_start_x + (i // 5) * (tank_width + column_spacing)
            left_tank_y = start_y + (i % 5) * (tank_height + tank_spacing)
           
            right_tank_x = right_start_x + (i // 5) * (tank_width + column_spacing)
            right_tank_y = start_y + (i % 5) * (tank_height + tank_spacing)

          
            tank_image_left = pygame.image.load(self.tanks[i])
            tank_image_left = pygame.transform.scale(tank_image_left, (tank_width, tank_height))
            self.screen.blit(tank_image_left, (left_tank_x, left_tank_y))

            
            tank_image_right = pygame.image.load(self.tanks[i + 10])
            tank_image_right = pygame.transform.scale(tank_image_right, (tank_width, tank_height))
            self.screen.blit(tank_image_right, (right_tank_x, right_tank_y))

            
            if self.selected_tanks[0] == self.tanks[i]:
                pygame.draw.rect(self.screen, (255, 0, 0), (left_tank_x - border_margin, left_tank_y - border_margin, tank_width + 2 * border_margin, tank_height + 2 * border_margin), border_thickness)

            
            if self.selected_tanks[1] == self.tanks[i + 10]:
                pygame.draw.rect(self.screen, (255, 0, 0), (right_tank_x - border_margin, right_tank_y - border_margin, tank_width + 2 * border_margin, tank_height + 2 * border_margin), border_thickness)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return None, None
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for i in range(10):
                    left_tank_rect = pygame.Rect(100 + (i // 5) * (60 + 80), 100 + (i % 5) * (60 + 20), 60, 60)
                    right_tank_rect = pygame.Rect(500 + (i // 5) * (60 + 80), 100 + (i % 5) * (60 + 20), 60, 60)
                    if left_tank_rect.collidepoint(mouse_pos):
                        self.selected_tanks[0] = self.tanks[i]
                        self.button_sound.play()
                    if right_tank_rect.collidepoint(mouse_pos):
                        self.selected_tanks[1] = self.tanks[i + 10]
                        self.button_sound.play()

                if self.confirm_button.collidepoint(mouse_pos):
                    if None not in self.selected_tanks:
                        self.running = False
                        self.button_sound.play()

                        return self.selected_tanks
                        

    def show(self):
        while self.running:
            self.handle_events()
            self.screen.fill((0, 0, 0))
            background_image = pygame.image.load(GRAPHICS_FOLDER +'background3.jpg')
            self.screen.blit(background_image, (0, 0))

            
            self.draw_tanks()
            pygame.draw.rect(self.screen, (0, 255, 0), self.confirm_button, border_radius=15)
            confirm_text = self.font.render("Confirm", True, (0, 0, 0))
            self.screen.blit(confirm_text, (self.confirm_button.x + 5, self.confirm_button.y + 5))
            
            pygame.display.flip()
            self.clock.tick(60)
        return self.selected_tanks

