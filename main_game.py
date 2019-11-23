import pygame
import random
from os import path


font_name = pygame.font.match_font('arial')
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

WIDTH = 1150
HEIGHT = 654
FPS = 60

# Estabelece a pasta que contem as figuras.
img_dir = path.join(path.dirname(__file__), 'game_files')
# Estabelece a pasta que contem os sons.
snd_dir = path.join(path.dirname(__file__), 'game_files')


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)
