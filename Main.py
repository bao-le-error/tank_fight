import pygame
from Code.Games import Menu

if __name__ == "__main__":
    """
    Hàm chính của chương trình, khởi tạo Pygame, tạo và hiển thị menu trò chơi, 
    sau đó kết thúc Pygame khi hoàn thành.

    - Khởi tạo Pygame.
    - Tạo đối tượng Menu từ module Code.Games.
    - Gọi phương thức show_menu() để hiển thị menu trò chơi.
    - Đóng Pygame khi thoát chương trình.
    """
    pygame.init()
    menu = Menu()
    menu.show_menu()
    pygame.quit()
