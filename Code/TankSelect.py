import pygame
from pygame.locals import *

# Thư mục chứa các tệp đồ họa, âm thanh và phông chữ
GRAPHICS_FOLDER = "Graphics/"
SOUND_FOLDER = "Sounds/"
FONT_FOLDER = "Font/"

class TankSelect:
    """Khởi tạo lớp TankSelect, thiết lập màn hình, đồng hồ, trạng thái chạy, các xe tăng, phông chữ, nút xác nhận, văn bản và âm thanh."""
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600)) # Thiết lập kích thước cửa sổ 
        pygame.display.set_caption('Select Tank') # Đặt tiêu đề cửa sổ trò chơi
        self.clock = pygame.time.Clock() # Tạo đồng hồ để điều chỉnh tốc độ khung hình
        self.running = True
        self.tanks = [GRAPHICS_FOLDER + '1.png', GRAPHICS_FOLDER + '4.png',GRAPHICS_FOLDER + '6.png',GRAPHICS_FOLDER + '7.png',GRAPHICS_FOLDER + '8.png',GRAPHICS_FOLDER + '11.png',GRAPHICS_FOLDER + '12.png',GRAPHICS_FOLDER + '20.png',GRAPHICS_FOLDER + '21.png',GRAPHICS_FOLDER + '23.png',
                      GRAPHICS_FOLDER + '2.png', GRAPHICS_FOLDER + '3.png',GRAPHICS_FOLDER + '5.png',GRAPHICS_FOLDER + '9.png',GRAPHICS_FOLDER + '10.png',GRAPHICS_FOLDER + '18.png',GRAPHICS_FOLDER + '13.png',GRAPHICS_FOLDER + '14.png',GRAPHICS_FOLDER + '15.png',GRAPHICS_FOLDER + '16.png']
        """ Danh sách đường dẫn tới các hình ảnh xe tăng"""
        self.selected_tanks = [None, None] # Lưu trữ xe tăng đã chọn cho người chơi 1 và 2
        self.font = pygame.font.Font(FONT_FOLDER + 'wheaton capitals.ttf', 30)
        self.confirm_button = pygame.Rect(325, 500, 150, 50)
        self.player1_text = self.font.render("Player 1", True, (255, 255, 255))
        self.player2_text = self.font.render("Player 2", True, (255, 255, 255))
        self.tank_select = self.font.render("Tank Select", True, (255, 255, 255))
        self.button_sound = pygame.mixer.Sound(SOUND_FOLDER +'button.mp3')
        """ Tiết lập các button, text tương ứng với cửa sổ"""
    def draw_tanks(self):
        """Vẽ các xe tăng lên màn hình và đánh dấu xe tăng đã chọn."""
        tank_width, tank_height = 60, 60 # Kích thước xe tăng
        tank_spacing = 20 # Khoảng cách giữa các xe tăng
        column_spacing = 80  # Khoảng cách giữa các cột xe tăng
        left_start_x = 100 # Vị trí bắt đầu của cột trái
        right_start_x = 500 # Vị trí bắt đầu của cột phải
        start_y = 110 # Vị trí bắt đầu của dòng xe tăng
        border_thickness = 3 # Độ dày của viền đánh dấu
        border_margin = 5 # Khoảng cách giữa viền và hình ảnh xe tăng

        # Vẽ văn bản cho người chơi 1 và 2 cùng với tiêu đề
        self.screen.blit(self.player1_text, (left_start_x + 50, start_y - 40))
        self.screen.blit(self.player2_text, (right_start_x + 50, start_y - 40))
        self.screen.blit(self.tank_select, (300, 10))
        
        for i in range(10):
            # Tính toán vị trí của xe tăng bên trái và bên phải
            left_tank_x = left_start_x + (i // 5) * (tank_width + column_spacing)
            left_tank_y = start_y + (i % 5) * (tank_height + tank_spacing)
           
            right_tank_x = right_start_x + (i // 5) * (tank_width + column_spacing)
            right_tank_y = start_y + (i % 5) * (tank_height + tank_spacing)

            # Vẽ xe tăng bên trái
            tank_image_left = pygame.image.load(self.tanks[i])
            tank_image_left = pygame.transform.scale(tank_image_left, (tank_width, tank_height))
            self.screen.blit(tank_image_left, (left_tank_x, left_tank_y))

            # Vẽ xe tăng bên phải
            tank_image_right = pygame.image.load(self.tanks[i + 10])
            tank_image_right = pygame.transform.scale(tank_image_right, (tank_width, tank_height))
            self.screen.blit(tank_image_right, (right_tank_x, right_tank_y))

            # Đánh dấu viền xe tăng đã chọn của người chơi 1
            if self.selected_tanks[0] == self.tanks[i]:
                pygame.draw.rect(self.screen, (255, 0, 0), (left_tank_x - border_margin, left_tank_y - border_margin, tank_width + 2 * border_margin, tank_height + 2 * border_margin), border_thickness)

            # Đánh dấu viền xe tăng đã chọn của người chơi 2
            if self.selected_tanks[1] == self.tanks[i + 10]:
                pygame.draw.rect(self.screen, (255, 0, 0), (right_tank_x - border_margin, right_tank_y - border_margin, tank_width + 2 * border_margin, tank_height + 2 * border_margin), border_thickness)

    def handle_events(self):
        """Xử lý các sự kiện, kiểm tra việc nhấn chuột và cập nhật xe tăng đã chọn."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Kiểm tra sự kiện thoát chương trình
                self.running = False
                return None, None
            if event.type == pygame.MOUSEBUTTONDOWN: # Kiểm tra sự kiện nhấn chuột
                mouse_pos = pygame.mouse.get_pos() # Lấy vị trí chuột
                for i in range(10):
                    # Tạo các hình chữ nhật đại diện cho vùng bấm chọn xe tăng
                    left_tank_rect = pygame.Rect(100 + (i // 5) * (60 + 80), 100 + (i % 5) * (60 + 20), 60, 60)
                    right_tank_rect = pygame.Rect(500 + (i // 5) * (60 + 80), 100 + (i % 5) * (60 + 20), 60, 60)
                    if left_tank_rect.collidepoint(mouse_pos): # Kiểm tra nếu vùng bấm chọn của xe tăng bên trái bị nhấn
                        self.selected_tanks[0] = self.tanks[i]
                        self.button_sound.play() # Phát âm thanh khi bấm nút
                    if right_tank_rect.collidepoint(mouse_pos): # Kiểm tra nếu vùng bấm chọn của xe tăng bên phải bị nhấn
                        self.selected_tanks[1] = self.tanks[i + 10]
                        self.button_sound.play() # Phát âm thanh khi bấm nút

                if self.confirm_button.collidepoint(mouse_pos): # Kiểm tra nếu nút xác nhận bị nhấn
                    if None not in self.selected_tanks: # Kiểm tra nếu cả hai xe tăng đã được chọn
                        self.running = False
                        self.button_sound.play() # Phát âm thanh khi bấm nút

                        return self.selected_tanks
                        

    def show(self):
        """Hiển thị màn hình chọn xe tăng, xử lý sự kiện và vẽ giao diện."""
        while self.running:
            self.handle_events()# Xử lý các sự kiện
            self.screen.fill((0, 0, 0)) # Đổ màu nền
            background_image = pygame.image.load(GRAPHICS_FOLDER +'background3.jpg') # Tải và vẽ ảnh nền
            self.screen.blit(background_image, (0, 0))
            self.draw_tanks() # Vẽ các xe tăng
            pygame.draw.rect(self.screen, (0, 255, 0), self.confirm_button, border_radius=15) # Vẽ nút xác nhận
            confirm_text = self.font.render("Confirm", True, (0, 0, 0)) # Vẽ văn bản trên nút xác nhận
            self.screen.blit(confirm_text, (self.confirm_button.x + 5, self.confirm_button.y + 5))
            
            pygame.display.flip() # Cập nhật màn hình
            self.clock.tick(120) # Điều chỉnh tốc độ khung hình
        return self.selected_tanks # Trả về danh sách xe tăng đã chọn
 
