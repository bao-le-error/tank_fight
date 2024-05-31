import pygame
import random
import sys


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
        self.rect.x = -100  # Move off-screen
        self.state = 'ready'



class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption('Tank Fight')
        self.clock = pygame.time.Clock()
        self.running = True
        self.background = pygame.image.load('road.png') 
        self.players = [Player('tank.png', random.randint(0, 300), random.randint(220, 460)),
                        Player('tank1.png', random.randint(500, 780), random.randint(220, 460))]
        self.bullets = [Bullet('bullet.png', 0, 0), Bullet('bullet2.png', 0, 0)]
        self.score_player1 = 0
        self.score_player2 = 0
        self.font = pygame.font.Font('wheaton capitals.ttf', 16)
        self.border_x = 400
        self.border_thickness = 10
        self.border = pygame.Rect(self.border_x - self.border_thickness // 2, 0, self.border_thickness, 600)
        self.back_button = pygame.Rect(120, 2, 70, 30)
        self.back_font = pygame.font.Font(None, 32)
    
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
                if event.key == pygame.K_RETURN:
                    if self.bullets[1].state == 'ready':
                        self.bullets[1].rect.x = self.players[1].rect.x + 11
                        self.bullets[1].rect.y = self.players[1].rect.y + 14
                        self.bullets[1].state = 'fire'
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
                        menu = Menu()
                        menu.show_menu()
    def update(self):
        for player in self.players:
            new_x = player.rect.x + player.x_change
            new_y = player.rect.y + player.y_change

            if player == self.players[0]:  # Left player
                if new_x < 0:
                    player.rect.x = 0
                elif new_x > self.border_x - player.rect.width:
                    player.rect.x = self.border_x - player.rect.width
                else:
                    player.rect.x = new_x
            else:  # Right player
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

        if pygame.Rect.colliderect(self.bullets[1].rect, self.players[0].rect):
            self.bullets[1].reset()
            self.score_player2 += 1
            self.players[0].rect.x = random.randint(0, 300)
            self.players[0].rect.y = random.randint(220, 460)

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        for player in self.players:
            self.screen.blit(player.image, player.rect)
        for bullet in self.bullets:
            if bullet.state == 'fire':
                self.screen.blit(bullet.image, bullet.rect)
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


class Menu:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption('Home')
        self.clock = pygame.time.Clock()
        self.running = True
        self.background = pygame.image.load('background2.jpg')
        self.button_sound = pygame.mixer.Sound('button.mp3')
        self.click_sound = pygame.mixer.Sound('click.mp3')
        self.music_timer = 0
        self.start_button = pygame.Rect(300, 420, 200, 60)
        self.exit_button = pygame.Rect(300, 520, 200, 60)
        self.credit_button = pygame.Rect(50, 460, 200, 60)
        self.control_button = pygame.Rect(550, 460, 200, 60)
        self.font = pygame.font.Font('wheaton capitals.ttf', 40)
        self.music_font = pygame.font.Font('wheaton capitals.ttf', 40)
        self.click = False
        self.logo = pygame.image.load('logo.png')
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
            if self.music_timer > 0:
                self.music_timer -= 1
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.logo, self.logo_rect)
            self.draw_button(self.start_button, 'Start', (255, 255, 255), (0, 128, 0), (0, 255, 0))  # Green button
            self.draw_button(self.exit_button, 'Exit', (255, 255, 255), (128, 0, 0), (255, 0, 0))  # Red button
            self.draw_button(self.credit_button, 'Author', (255, 255, 255), (0, 0, 128), (0, 0, 255))  # Blue button
            self.draw_button(self.control_button, 'Control', (255, 255, 255), (255, 140, 0), (255, 255, 0))      
            pygame.display.update()
            self.clock.tick(60)



    def draw_button(self, rect, text, text_color, normal_color, hover_color):
        mx, my = pygame.mouse.get_pos()
        mouse = pygame.Rect(mx, my, 1, 1)

        shadow_offset = 5
        shadow_color = (50, 50, 50)
        button_color = normal_color if not rect.collidepoint((mx, my)) else hover_color

        # Draw shadow
        shadow_rect = rect.move(shadow_offset, shadow_offset)
        pygame.draw.rect(self.screen, shadow_color, shadow_rect, border_radius=15)

        # Draw button
        pygame.draw.rect(self.screen, button_color, rect, border_radius=15)
        
        if rect.collidepoint((mx, my)):
            if self.click:
                self.button_sound.play()
                if rect == self.start_button:
                    game = Game()
                    game.start()
                elif rect == self.exit_button:
                    self.running = False
                elif rect == self.credit_button:
                    self.show_author()
                elif rect == self.control_button:
                    self.show_controls()

        button_font = self.font 
        text_render = button_font.render(text, True, text_color)
        self.screen.blit(text_render, (rect.x + rect.width // 2 - text_render.get_width() // 2,
                                       rect.y + rect.height // 2 - text_render.get_height() // 2))

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
            control_text = ["Player 1: W, A, S, D to move, N to shoot",
                            "Player 2: Arrow keys to move, Enter to shoot"]
            for i, line in enumerate(control_text):
                text = self.font.render(line, True, (255, 255, 255))
                self.screen.blit(text, (400 - text.get_width() // 2, 100 + i * 40))
            pygame.draw.rect(self.screen, (255, 0, 0), back_button, border_radius=15)

            back_text = self.font.render("Back", True, (255, 255, 255))
            self.screen.blit(back_text, (back_button.x + 10, back_button.y + 2))
            pygame.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    pygame.init()  
    menu = Menu()
    menu.__init__()  # Initialize the Menu class
    menu.show_menu()
    pygame.quit()
