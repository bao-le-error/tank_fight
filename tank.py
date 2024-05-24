
import pygame
import random

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

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption('Game bắn tank đỉnh cao :))')
        self.clock = pygame.time.Clock()
        self.running = True
        self.background = pygame.image.load('road.png')
        self.players = [Player('tank.png', random.randint(0, 500), random.randint(220, 460)),
                        Player('tank1.png', random.randint(600, 780), random.randint(220, 460))]
        self.bullets = [Bullet('bullet.png', 0, 0), Bullet('bullet2.png', 0, 0)]
        self.score_player1 = 0
        self.score_player2 = 0
        self.font = pygame.font.Font('freesansbold.ttf', 16)
        self.border_x = 400
        self.border_thickness = 5
        self.border = pygame.Rect(self.border_x - self.border_thickness // 2, 0, self.border_thickness, 600)
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
                if event.key == pygame.K_n or event.key == pygame.K_SPACE:
                    if self.bullets[0].state == 'ready':
                        self.bullets[0].rect.x = self.players[0].rect.x + 11
                        self.bullets[0].rect.y = self.players[0].rect.y + 14
                        self.bullets[0].state = 'fire'
                if event.key == pygame.K_BACKSPACE or event.key == pygame.K_RETURN:
                    if self.bullets[1].state == 'ready':
                        self.bullets[1].rect.x = self.players[1].rect.x + 11
                        self.bullets[1].rect.y = self.players[1].rect.y + 14
                        self.bullets[1].state = 'fire'
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_s or event.key == pygame.K_w:
                    self.players[0].y_change = 0
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    self.players[0].x_change = 0
                if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                    self.players[1].y_change = 0
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    self.players[1].x_change = 0


    def update(self):
        
        for player in self.players:
            player.rect.x += player.x_change
            player.rect.y += player.y_change
            if player.rect.x <= 0:
                player.rect.x = 0
            elif player.rect.x >= 736:
                player.rect.x = 736
            if player.rect.y <= 200:
                player.rect.y = 200
            elif player.rect.y >= 460:
                player.rect.y = 460
        for bullet in self.bullets:
            if bullet.state == 'fire':
                bullet.rect.x += 15 if bullet == self.bullets[0] else -15
                if bullet.rect.x <= 0 or bullet.rect.x >= 800:
                    bullet.state = 'ready'
        if pygame.Rect.colliderect(self.bullets[0].rect, self.players[1].rect):
            self.bullets[0].state = 'ready'
            self.score_player1 += 1
            self.players[1].rect.x = random.randint(600, 780)
            self.players[1].rect.y = random.randint(220, 460)
        if pygame.Rect.colliderect(self.bullets[1].rect, self.players[0].rect):
            self.bullets[1].state = 'ready'
            self.score_player2 += 1
            self.players[0].rect.x = random.randint(0, 500)
            self.players[0].rect.y = random.randint(220, 460)
        
    def draw(self):
        self.screen.blit(self.background, (0, 0))
        for player in self.players:
            self.screen.blit(player.image, player.rect)
        for bullet in self.bullets:
            if bullet.state == 'fire':
                self.screen.blit(bullet.image, bullet.rect)
        score1 = self.font.render("Player1: " + str(self.score_player1), True, (255, 255, 255))
        score2 = self.font.render("Player2: " + str(self.score_player2), True, (255, 255, 255))
        self.screen.blit(score1, (0, 0))
        self.screen.blit(score2, (0, 18))
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
        self.background = pygame.image.load('background.jpg')
        self.button_sound = pygame.mixer.Sound('button.mp3')
        self.click_sound = pygame.mixer.Sound('click.mp3')
        self.music1 = [pygame.mixer.Sound('music1.mp3'), pygame.mixer.Sound('music2.mp3'),
                       pygame.mixer.Sound('music3.mp3')]
        self.music1[0].set_volume(0.3)
        self.music1[1].set_volume(0.3)
        self.music1[2].set_volume(0.3)
        self.music_timer = 0
        self.start_button = pygame.Rect(250, 160, 300, 60)
        self.exit_button = pygame.Rect(250, 260, 300, 60)
        self.credit_button = pygame.Rect(100, 360, 250, 60)
        self.music_button = pygame.Rect(450, 360, 250, 60)
        self.stop_button = pygame.Rect(710, 360, 50, 60)
        self.control_button = pygame.Rect(250, 460, 300, 60)
        self.font = pygame.font.Font('freesansbold.ttf', 40)
        self.music_font = pygame.font.Font('freesansbold.ttf', 25)
        self.click = False

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
            self.draw_button(self.start_button, 'Start', (255, 255, 255), (0, 100, 0), (16, 176, 16))
            self.draw_button(self.exit_button, 'Exit', (255, 255, 255), (100, 0, 0), (227, 5, 27))
            self.draw_button(self.credit_button, 'Author', (255, 255, 255), (0, 100, 0), (16, 176, 16))
            self.draw_button(self.music_button, 'Play Music', (255, 255, 255), (0, 100, 0), (16, 176, 16))
            self.draw_button(self.stop_button, 'll', (255, 255, 255), (100, 0, 0), (227, 5, 27))
            self.draw_button(self.control_button, 'Control', (255, 255, 255), (0, 100, 0), (16, 176, 16))
            pygame.display.update()
            self.clock.tick(60)

    def draw_button(self, rect, text, text_color, normal_color, hover_color):
        mx, my = pygame.mouse.get_pos()
        mouse = pygame.Rect(mx, my, 1, 1)
        pygame.draw.rect(self.screen, normal_color if not rect.collidepoint((mx, my)) else hover_color, rect)
        if rect.collidepoint((mx, my)):
            if self.click:
                self.button_sound.play()
                if rect == self.start_button:
                    print("Start button clicked")
                    game = Game()
                    game.start()
                elif rect == self.exit_button:
                    print("Exit button clicked")
                    self.running = False
                elif rect == self.credit_button:
                    print("Author button clicked")
                    # Gọi hàm hiển thị tác giả ở đây
                elif rect == self.music_button:
                    print("Music button clicked")
                    # Gọi hàm phát nhạc ở đây
                    if self.music_timer == 0:
                        pygame.mixer.stop()
                        self.music_timer = 120
                        random.choice(self.music1).play()
                        self.click_sound.play()
                elif rect == self.stop_button:
                    print("Stop button clicked")
                    pygame.mixer.fadeout(1000)
                elif rect == self.control_button:
                    print("Control button clicked")
                    # Gọi hàm hiển thị hướng dẫn điều khiển ở đây
        button_font = self.font if rect != self.music_button else self.music_font
        text_render = button_font.render(text, True, text_color)
        self.screen.blit(text_render, (rect.x + rect.width // 2 - text_render.get_width() // 2,
                                       rect.y + rect.height // 2 - text_render.get_height() // 2))

if __name__ == "__main__":
    menu = Menu()
    menu.show_menu()
    pygame.quit()