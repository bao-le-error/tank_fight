# Khởi tạo các thư viện để sử dụng cho game
import pygame
import random
# Truy cập và sử dụng các module
from .Players import Player
from .Bullets import Bullet
from .TankSelect import TankSelect

# Khai báo các thư mục chứa hình ảnh, âm thanh và font chữ cho game
GRAPHICS_FOLDER = "Graphics/"
SOUND_FOLDER = "Sounds/"
FONT_FOLDER = "Font/"

# Lớp đại diện cho trò chơi
class Game:
    def __init__(self, player1_tank, player2_tank):
        self.screen = pygame.display.set_mode((800, 600)) # Thiết lập cửa sổ trò chơi
        pygame.display.set_caption('Tank Fight') # Đặt tiêu đề cho cửa sổ trò chơi
        self.clock = pygame.time.Clock() # Tạo đối tượng đồng hồ để điều khiển tốc độ khung hình
        self.running = True # Trạng thái của trò chơi
        self.background = pygame.image.load(GRAPHICS_FOLDER +'road.png') # Tải hình nền
        self.players = [Player(player1_tank, random.randint(0, 300), random.randint(220, 460)),
                        Player(player2_tank, random.randint(500, 780), random.randint(220, 460))] # Tạo hai người chơi với vị trí ngẫu nhiên
        self.bullets = [Bullet(GRAPHICS_FOLDER +'bullet.png', 0, 0), Bullet(GRAPHICS_FOLDER +'bullet2.png', 0, 0)] # Tạo hai viên đạn
        # Khởi tạo điểm số bắt đầu của 2 người chơi
        self.score_player1 = 0
        self.score_player2 = 0
        self.font = pygame.font.Font(FONT_FOLDER + 'wheaton capitals.ttf', 16) # Thiết lập font chữ
        self.border_x = 400 # Vị trí x của biên giới giữa hai bên
        self.border_thickness = 10 # Độ dày của biên giới
        self.border = pygame.Rect(self.border_x - self.border_thickness // 2, 0, self.border_thickness, 600)  # Tạo hình chữ nhật cho biên giới
        self.back_button = pygame.Rect(120, 2, 70, 30) # Tạo hình chữ nhật cho nút quay lại
        self.back_font = pygame.font.Font(None, 32) # Tải font chữ cho nút quay lại
        self.boom = pygame.mixer.Sound(SOUND_FOLDER +'boom.wav')  # Tải âm thanh nổ
        self.shoot = pygame.mixer.Sound(SOUND_FOLDER +'tankshot.wav') # Tải âm thanh bắn súng
        pygame.mixer.music.load(SOUND_FOLDER + 'background.mp3') # Tải nhạc nền
        pygame.mixer.music.play(-1) # Phát nhạc nền lặp lại
        self.bang = pygame.image.load(GRAPHICS_FOLDER +'bang.png') # Tải hình ảnh nổ
        self.hit_position = None # Thiết lập vị trí va chạm
        self.hit_timer = 0 # Thiết lập bộ đếm thời gian va chạm
        self.score_limit = 20 # Giới hạn điểm để chiến thắng
        self.winner = None # Người chiến thắng
        self.font_winner = pygame.font.Font(FONT_FOLDER + 'wheaton capitals.ttf', 100)  # Tải font chữ cho người chiến thắng
        self.button_sound = pygame.mixer.Sound(SOUND_FOLDER +'button.mp3') # Tải âm thanh nút
        self.winner_sound = pygame.mixer.Sound(SOUND_FOLDER +'winner.mp3') # Tải âm thanh chiến thắng

    def handle_events(self):
        # Xử lý sự kiện trong trò chơi
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False # Thoát trò chơi khi nhấn nút đóng cửa sổ
            if event.type == pygame.KEYDOWN:
                # Xử lý các phím thao tác của người chơi, bao gồm di chuyển và bắn
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
                        self.shoot.play() # Phát âm thanh bắn súng khi người chơi 1 bắn
                if event.key == pygame.K_RETURN:
                    if self.bullets[1].state == 'ready':
                        self.bullets[1].rect.x = self.players[1].rect.x + 11
                        self.bullets[1].rect.y = self.players[1].rect.y + 14
                        self.bullets[1].state = 'fire'
                        self.shoot.play() # Phát âm thanh bắn súng khi người chơi 2 bắn
            if event.type == pygame.KEYUP:
                # Xử lý các phím được thả
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
                        self.running = False # Thoát trò chơi khi nhấn nút quay lại
                        pygame.mixer.music.stop()  
                        menu = Menu()
                        menu.show_menu() # Hiển thị menu chính
                        

    def update(self):
        # Cập nhật trạng thái trò chơi, vị trí của người chơi và vị trí của viên đạn
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
        # Thiết lập vị trí random của tank khi bị bắn trúng
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
        # Thiết lập trạng thái chiến thắng cho người chơi
        if self.score_player1 >= self.score_limit:
            self.winner = "Player 1"
            self.show_winner()
            self.running = False
        elif self.score_player2 >= self.score_limit:
            self.winner = "Player 2"
            self.show_winner()
            self.running = False

    def show_winner(self): # Khởi tạo hàm cho trạng thái chiến thắng của người chơi
        pygame.mixer.music.stop() # Dừng nhạc nền của trạng thái chơi game
        self.winner_sound.play() # Phát âm thanh nền chiến thắng
        winner_running = True
        # Khởi tạo các button trong cửa sổ, đồng thời thêm background cho cửa sổ đó
        back_to_menu_button = pygame.Rect(300, 400, 165, 35)
        play_again_button = pygame.Rect(300, 470, 165, 35)
        winner_background = pygame.image.load(GRAPHICS_FOLDER +'winner.gif')   
        winner_background = pygame.transform.scale(winner_background, (800, 600)) 
        # Các trạng thái hoạt động dành cho người chơi khi cửa sổ chiến thắng được hiển thị
        while winner_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    winner_running = False
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pos = pygame.mouse.get_pos()
                        # Nhấn button Back to menu để về Menu
                        if back_to_menu_button.collidepoint(mouse_pos):
                            self.button_sound.play()
                            winner_running = False
                            self.running = False
                            self.winner_sound.stop()
                            menu = Menu()
                            menu.show_menu()
                        # Nhấn button Play again để chơi lại và được chọn tank
                        elif play_again_button.collidepoint(mouse_pos):
                            self.button_sound.play()
                            winner_running = False
                            self.running = False
                            self.winner_sound.stop()
                            tank_select = TankSelect()
                            selected_tanks = tank_select.show()
                            if selected_tanks and None not in selected_tanks:
                                self.__init__(selected_tanks[0], selected_tanks[1])
                                self.start()
            # Thiết lập background, button, text của button cho cửa sổ
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
            self.clock.tick(120)

        
    def draw(self): # Hàm draw, thiết lập các hoạt động như bắn, trở về, và tăng số điểm nếu người chơi bắn trúng tank địch
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
        # Chạy trò chơi
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(120)
        pygame.quit()

class Menu:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600)) # Thiết lập cửa sổ trò chơi
        pygame.display.set_caption('Home') 
        self.clock = pygame.time.Clock() # Tạo đối tượng đồng hồ để điều khiển tốc độ khung hình
        self.running = True # Trạng thái của menu
        # Thiết lập các đối tượng hình ảnh, âm thanh và button
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
        #Xử lý các sự kiện trong menu, bao gồm các sự kiện thoát,nhấp chuột và thả chuột.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False  # Thoát menu khi nhấn nút đóng cửa sổ
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.click_sound.play()
                if event.button == 1:
                    self.click = True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.click = False

    def show_menu(self): #Hiển thị menu chính và xử lý các sự kiện liên quan đến menu.
        while self.running:
            self.handle_events()
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.logo, self.logo_rect)
            self.draw_button(self.start_button, 'Start', (255, 255, 255), (0, 128, 0), (0, 255, 0))  
            self.draw_button(self.exit_button, 'Exit', (255, 255, 255), (128, 0, 0), (255, 0, 0)) 
            self.draw_button(self.credit_button, 'Author', (255, 255, 255), (0, 0, 128), (0, 0, 255)) 
            self.draw_button(self.control_button, 'Control', (255, 255, 255), (255, 140, 0), (255, 255, 0))      
            pygame.display.update()
            self.clock.tick(120)

    def draw_button(self, rect, text, text_color, normal_color, hover_color):
        """
        Vẽ button trên màn hình và xử lý các sự kiện liên quan đến button.

        Args:
            rect (pygame.Rect): Hình chữ nhật đại diện cho button.
            text (str): Văn bản hiển thị trên button.
            text_color (tuple): Màu của văn bản.
            normal_color (tuple): Màu của button khi không được hover.
            hover_color (tuple): Màu của button khi được hover.
        """
        mx, my = pygame.mouse.get_pos()
        mouse = pygame.Rect(mx, my, 1, 1)

        shadow_offset = 5
        shadow_color = (50, 50, 50)
        button_color = normal_color if not rect.collidepoint((mx, my)) else hover_color
        shadow_rect = rect.move(shadow_offset, shadow_offset)

        pygame.draw.rect(self.screen, shadow_color, shadow_rect, border_radius=15)
        pygame.draw.rect(self.screen, button_color, rect, border_radius=15)
        # Xử lí các thao tác của người chơi với các button tương ứng
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

    def show_author(self): # Thiết lập hàm hiển thị cửa sổ tác giả của game
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
            text = self.font.render("Author:LE NGUYEN QUOC BAO ", True, (255, 255, 255))
            
            self.screen.blit(text, (400 - text.get_width() // 2, 300 - text.get_height() // 2))
            pygame.draw.rect(self.screen, (255, 0, 0), back_button, border_radius=15)

            back_text = self.font.render("Back", True, (255, 255, 255))
            self.screen.blit(back_text, (back_button.x + 10, back_button.y + 2))
            pygame.display.flip()
            self.clock.tick(120)

    def show_controls(self): # Thiết lập hàm hiển thị cửa sổ hướng dẫn chơi game 
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
                "Enter - Shoot",
                "",
                "WINNER ????",
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
            self.clock.tick(120)
