import pygame
from Code.Games import Menu

if __name__ == "__main__":
    pygame.init()
    menu = Menu()
    menu.show_menu()
    pygame.quit()
