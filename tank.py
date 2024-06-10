import pygame
import random


pygame.init()
GRAPHICS_FOLDER = "Graphics/"
SOUND_FOLDER = "Sounds/"
FONT_FOLDER = "Font/"


class Player:
    def __init__(self, image, x, y):
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x_change = 0
        self.y_change = 0

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

class Game:
    def __init__(self, player1_tank, player2_tank):
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption('Tank Fight')
        self.clock = pygame.time.Clock()
        self.running = True
        self.background = pygame.image.load(GRAPHICS_FOLDER +'road.png') 
        self.players = [Player(player1_tank, random.randint(0, 300), random.randint(220, 460)),
                        Player(player2_tank, random.randint(500, 780), random.randint(220, 460))]
        self.bullets = [Bullet(GRAPHICS_FOLDER +'bullet.png', 0, 0), Bullet(GRAPHICS_FOLDER +'bullet2.png', 0, 0)]
        self.score_player1 = 0
        self.score_player2 = 0
        self.font = pygame.font.Font(FONT_FOLDER + 'wheaton capitals.ttf', 16)
        self.border_x = 400
        self.border_thickness = 10
        self.border = pygame.Rect(self.border_x - self.border_thickness // 2, 0, self.border_thickness, 600)
        self.back_button = pygame.Rect(120, 2, 70, 30)
        self.back_font = pygame.font.Font(None, 32)
        self.boom = pygame.mixer.Sound(SOUND_FOLDER +'boom.wav')
        self.shoot = pygame.mixer.Sound(SOUND_FOLDER +'tankshot.wav')
        pygame.mixer.music.load(SOUND_FOLDER + 'background.mp3')
        pygame.mixer.music.play(-1) 
        self.bang = pygame.image.load(GRAPHICS_FOLDER +'bang.png') 
        self.hit_position = None
        self.hit_timer = 0
        self.score_limit = 20
        self.winner = None
        self.font_winner = pygame.font.Font(FONT_FOLDER + 'wheaton capitals.ttf', 100)
        self.button_sound = pygame.mixer.Sound(SOUND_FOLDER +'button.mp3')
        self.winner_sound = pygame.mixer.Sound(SOUND_FOLDER +'winner.mp3')

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    self.players[0].y_change = 3.5
                if event.key == pygame.K_w:
                    self.players[0].y_change = -3.5
                if event.key == pygame.K_a:
                    self.players[0].x_change = -3.5
                if event.key == pygame.K_d:
                    self.players[0].x_change = 3.5
                if event.key == pygame.K_DOWN:
                    self.players[1].y_change = 3.5
                if event.key == pygame.K_UP:
                    self.players[1].y_change = -3.5
                if event.key == pygame.K_LEFT:
                    self.players[1].x_change = -3.5
                if event.key == pygame.K_RIGHT:
                    self.players[1].x_change = 3.5
                if event.key == pygame.K_SPACE:
                    if self.bullets[0].state == 'ready':
                        self.bullets[0].rect.x = self.players[0].rect.x + 11
                        self.bullets[0].rect.y = self.players[0].rect.y + 14
                        self.bullets[0].state = 'fire'
                        self.shoot.play()
                if event.key == pygame.K_RETURN:
                    if self.bullets[1].state == 'ready':
                        self.bullets[1].rect.x = self.players[1].rect.x + 11
                        self.bullets[1].rect.y = self.players[1].rect.y + 14
                        self.bullets[1].state = 'fire'
                        self.shoot.play()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_s and self.players[0].y_change > 0:
                    self.players[0].y_change = 0
                elif event.key == pygame.K_w and self.players[0].y_change < 0:
                    self.players[0].y_change = 0
                elif event.key == pygame.K_a and self.players[0].x_change < 0:
                    self.players[0].x_change = 0
                elif event.key == pygame.K_d and self.players[0].x_change > 0:
                    self.players[0].x_change = 0
                elif event.key == pygame.K_DOWN and self.players[1].y_change > 0:
                    self.players[1].y_change = 0
                elif event.key == pygame.K_UP and self.players[1].y_change < 0:
                    self.players[1].y_change = 0
                elif event.key == pygame.K_LEFT and self.players[1].x_change < 0:
                    self.players[1].x_change = 0
                elif event.key == pygame.K_RIGHT and self.players[1].x_change > 0:
                    self.players[1].x_change = 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.back_button.collidepoint(mouse_pos):
                        self.running = False
                        pygame.mixer.music.stop()  
                        menu = Menu()
                        menu.show_menu()

    def update(self):
        for player in self.players:
            new_x = player.rect.x + player.x_change
            new_y = player.rect.y + player.y_change
            
            if player == self.players[0]:  
                if new_x < 0:
                    player.rect.x = 0
                elif new_x > self.border_x - player.rect.width:
                    player.rect.x = self.border_x - player.rect.width
                else:
                    player.rect.x = new_x
            else: 
                if new_x < self.border_x:
                    player.rect.x = self.border_x
                elif new_x > 800 - player.rect.width:
                    player.rect.x = 800 - player.rect.width
                else:
                    player.rect.x = new_x

            if new_y < 200:
                player.rect.y = 200
            elif new_y > 460:
                player.rect.y = 460
            else:
                player.rect.y = new_y

        for bullet in self.bullets:
            if bullet.state == 'fire':
                bullet.rect.x += 15 if bullet == self.bullets[0] else -15
                if bullet.rect.x <= 0 or bullet.rect.x >= 800:
                    bullet.reset()

        if pygame.Rect.colliderect(self.bullets[0].rect, self.players[1].rect):
            self.bullets[0].reset()
            self.score_player1 += 1
            self.players[1].rect.x = random.randint(500, 780)
            self.players[1].rect.y = random.randint(220, 460)
            self.boom.play()
            self.hit_position = self.players[1].rect.center
            self.hit_timer = pygame.time.get_ticks()
        if pygame.Rect.colliderect(self.bullets[1].rect, self.players[0].rect):
            self.bullets[1].reset()
            self.score_player2 += 1
            self.players[0].rect.x = random.randint(0, 300)
            self.players[0].rect.y = random.randint(220, 460)
            self.boom.play()
            self.hit_position = self.players[0].rect.center
            self.hit_timer = pygame.time.get_ticks()
        if self.score_player1 >= self.score_limit:
            self.winner = "Player 1"
            self.show_winner()
            self.running = False
        elif self.score_player2 >= self.score_limit:
            self.winner = "Player 2"
            self.show_winner()
            self.running = False

    def show_winner(self):
        pygame.mixer.music.stop()  
        self.winner_sound.play()
        winner_running = True
        back_to_menu_button = pygame.Rect(300, 400, 165, 35)
        play_again_button = pygame.Rect(300, 470, 165, 35)
        winner_background = pygame.image.load(GRAPHICS_FOLDER +'winner.gif')   
        winner_background = pygame.transform.scale(winner_background, (800, 600)) 
        while winner_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    winner_running = False
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pos = pygame.mouse.get_pos()
                        if back_to_menu_button.collidepoint(mouse_pos):
                            self.button_sound.play()
                            winner_running = False
                            self.running = False
                            self.winner_sound.stop()
                            menu = Menu()
                            menu.show_menu()
                        elif play_again_button.collidepoint(mouse_pos):
                            self.button_sound.play()
                            self.winner_sound.stop()
                            winner_running = False
                            self.running = False
                            tank_select = TankSelect()
                            selected_tanks = tank_select.show()
                            if selected_tanks and None not in selected_tanks:
                                self.__init__(selected_tanks[0], selected_tanks[1])
                                self.start()

            self.screen.blit(winner_background, (0, 0)) 
            winner_text = self.font_winner.render(f"{self.winner}", True, (255, 255, 255))
            self.screen.blit(winner_text, (400 - winner_text.get_width() // 2, 150 - winner_text.get_height() // 2))
            pygame.draw.rect(self.screen, (255, 0, 0), back_to_menu_button, border_radius=8)
            pygame.draw.rect(self.screen, (0, 255, 0), play_again_button, border_radius=8)
            back_text = self.back_font.render("Back to Menu", True, (255, 255, 255))
            play_again_text = self.back_font.render("Play Again", True, (255, 255, 255))
            self.screen.blit(back_text, (back_to_menu_button.x + 10, back_to_menu_button.y + 7))
            self.screen.blit(play_again_text, (play_again_button.x + 25, play_again_button.y + 5))
            pygame.display.flip()
            self.clock.tick(60)

        
    def draw(self):
        self.screen.blit(self.background, (0, 0))
        for player in self.players:
            self.screen.blit(player.image, player.rect)
        for bullet in self.bullets:
            if bullet.state == 'fire':
                self.screen.blit(bullet.image, bullet.rect)
        if self.hit_position and pygame.time.get_ticks() - self.hit_timer < 100:   
            bang_rect = self.bang.get_rect(center=self.hit_position)
            self.screen.blit(self.bang, bang_rect)
        pygame.draw.rect(self.screen, (255, 0, 0), self.back_button, border_radius=8)
        back_text = self.back_font.render("Back", True, (255, 255, 255))
        self.screen.blit(back_text, (self.back_button.x + 10, self.back_button.y + 5))
        score1 = self.font.render("Player1: " + str(self.score_player1), True, (255, 255, 255))
        score2 = self.font.render("Player2: " + str(self.score_player2), True, (255, 255, 255))
        self.screen.blit(score1, (2, 0))
        self.screen.blit(score2, (2, 15))
        pygame.display.flip()

    def start(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
        pygame.quit()
        
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


class Menu:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption('Home')
        self.clock = pygame.time.Clock()
        self.running = True
        self.background = pygame.image.load(GRAPHICS_FOLDER +'background1.jpg')
        self.button_sound = pygame.mixer.Sound(SOUND_FOLDER +'button.mp3')
        self.click_sound = pygame.mixer.Sound(SOUND_FOLDER +'click.mp3')
        self.start_button = pygame.Rect(300, 420, 200, 60)
        self.exit_button = pygame.Rect(300, 520, 200, 60)
        self.credit_button = pygame.Rect(50, 460, 200, 60)
        self.control_button = pygame.Rect(550, 460, 200, 60)
        self.font = pygame.font.Font(FONT_FOLDER + 'wheaton capitals.ttf', 40)
        self.click = False
        self.logo = pygame.image.load(GRAPHICS_FOLDER +'logo.png')
        self.logo_rect = self.logo.get_rect(center =(425, 200))
        self.logo = pygame.transform.scale(self.logo, (750, 250))
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.click_sound.play()
                if event.button == 1:
                    self.click = True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.click = False

    def show_menu(self):
        while self.running:
            self.handle_events()
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.logo, self.logo_rect)
            self.draw_button(self.start_button, 'Start', (255, 255, 255), (0, 128, 0), (0, 255, 0))  
            self.draw_button(self.exit_button, 'Exit', (255, 255, 255), (128, 0, 0), (255, 0, 0)) 
            self.draw_button(self.credit_button, 'Author', (255, 255, 255), (0, 0, 128), (0, 0, 255)) 
            self.draw_button(self.control_button, 'Control', (255, 255, 255), (255, 140, 0), (255, 255, 0))      
            pygame.display.update()
            self.clock.tick(60)

    def draw_button(self, rect, text, text_color, normal_color, hover_color):
        mx, my = pygame.mouse.get_pos()
        mouse = pygame.Rect(mx, my, 1, 1)

        shadow_offset = 5
        shadow_color = (50, 50, 50)
        button_color = normal_color if not rect.collidepoint((mx, my)) else hover_color
        shadow_rect = rect.move(shadow_offset, shadow_offset)

        pygame.draw.rect(self.screen, shadow_color, shadow_rect, border_radius=15)
        pygame.draw.rect(self.screen, button_color, rect, border_radius=15)
        
        if rect.collidepoint((mx, my)):
            if self.click:
                self.button_sound.play()
                if rect == self.start_button:
                    tank_select = TankSelect()
                    selected_tanks = tank_select.show()
                    if selected_tanks and None not in selected_tanks:
                        game = Game(selected_tanks[0], selected_tanks[1])
                        game.start()
                elif rect == self.exit_button:
                    self.running = False
                elif rect == self.credit_button:
                    self.show_author()
                elif rect == self.control_button:
                    self.show_controls()

        text_surface = self.font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)

    def show_author(self):
        author_running = True
        back_button = pygame.Rect(10, 10, 130, 55)
        while author_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    author_running = False
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pos = pygame.mouse.get_pos()
                        if back_button.collidepoint(mouse_pos):
                            author_running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    author_running = False

            self.screen.fill((0, 0, 0))
            text = self.font.render("Author: LNQBR", True, (255, 255, 255))
            
            self.screen.blit(text, (400 - text.get_width() // 2, 300 - text.get_height() // 2))
            pygame.draw.rect(self.screen, (255, 0, 0), back_button, border_radius=15)

            back_text = self.font.render("Back", True, (255, 255, 255))
            self.screen.blit(back_text, (back_button.x + 10, back_button.y + 2))
            pygame.display.flip()
            self.clock.tick(60)

    def show_controls(self):
        control_running = True
        back_button = pygame.Rect(10, 10, 130, 55)
        control_font = pygame.font.Font(FONT_FOLDER + 'wheaton capitals.ttf', 24) 

        while control_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    control_running = False
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pos = pygame.mouse.get_pos()
                        if back_button.collidepoint(mouse_pos):
                            control_running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    control_running = False

            self.screen.fill((0, 0, 0))

            control_text = [
                "Player 1 Controls:",
                "W - Move Up",
                "S - Move Down",
                "A - Move Left",
                "D - Move Right",
                "Space - Shoot",
                "",
                "Player 2 Controls:",
                "Up Arrow - Move Up",
                "Down Arrow - Move Down",
                "Left Arrow - Move Left",
                "Right Arrow - Move Right",
                "Enter - Shoot"
                "",
                "WINNER ????"
                "Reach 20 to win the game",
            ]

            start_y = 100
            line_height = 30
    
            for i, line in enumerate(control_text):
                text = control_font.render(line, True, (255, 255, 255))
                text_rect = text.get_rect(center=(400, start_y + i * line_height))
                self.screen.blit(text, text_rect)

            pygame.draw.rect(self.screen, (255, 0, 0), back_button, border_radius=15)
            back_text = self.font.render("Back", True, (255, 255, 255))
            self.screen.blit(back_text, (back_button.x + 10, back_button.y + 2))
            pygame.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    pygame.init()
    menu = Menu()
    menu.show_menu()
    pygame.quit()
