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
    

    class Players(pygame.sprite.Sprite):
    def __init__(self, posicao):
        pygame.sprite.Sprite.__init__(self)
        player1_img = pygame.image.load(path.join(img_dir, 'luva_player_1.png'))  # Define imagem do Player1
        player2_img = pygame.image.load(path.join(img_dir, 'luva_player_2.png'))  # Define imagem do Player2

        self.image = pygame.transform.scale(player1_img, (80, 80))  # Define Proporções
        self.image.set_colorkey(BLACK)  # Deixa Transparente

        self.rect = self.image.get_rect()  # Obtem detalhes da posição

        if posicao == "esquerda":
            self.image = player1_img
            self.image = pygame.transform.scale(player1_img, (80, 80))  # Define Proporções
            self.rect.centerx = WIDTH - 980  # Posiciona no centro em x

        elif posicao == "direita":
            self.image = player2_img
            self.image = pygame.transform.scale(player2_img, (80, 80))  # Define Proporções
            self.rect.centerx = WIDTH - 175  # Posiciona no centro em x

        self.rect.bottom = HEIGHT / 2  # Posiciona objeto na parte inferior em y

        self.speedy = 0

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0
