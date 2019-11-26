import pygame
import random
from os import path
import socket

#############################################################################
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(('localhost', 8089))
serversocket.listen(5)  # become a server socket, maximum 5 connections
#############################################################################

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


##############################################################################
def conversor_buffer(texto_coordenadas):

    coordenadas_separadas = texto_coordenadas.split(", ")

    coordenada_0 = coordenadas_separadas[0].split("[")
    coordenada_j1 = coordenada_0[1]

    coordenada_1 = coordenadas_separadas[1].split("]")
    coordenada_j2 = coordenada_1[0]

    coordenada_j1 = int(coordenada_j1)

    coordenada_j2 = int(coordenada_j2)

    return coordenada_j1, coordenada_j2


###############################################################################

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


    def update(self):
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        ball = pygame.image.load(path.join(img_dir, 'ball.png'))  # Define imagem do Player
        self.image = ball  # Coloca imagem do Player

        self.image = pygame.transform.scale(ball, (40, 40))  # Define Proporções
        self.image.set_colorkey(BLACK)  # Deixa Transparente
        self.rect = self.image.get_rect()  # Obtem detalhes da posição

        self.radius = 20

        self.rect.x = 0
        self.rect.y = 0

        self.speedx = 0
        self.speedy = 0

        self.reset()

    def reset(self):
        self.rect.x = WIDTH / 2  # Posiciona no centro em x
        self.rect.y = HEIGHT / 2  # Posiciona objeto no centro em y
        self.speedx = random.choice([-5, 5])
        self.speedy = random.randrange(-5, 5)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if self.rect.right > WIDTH:
            self.speedx = -8
        if self.rect.left < 0:
            self.speedx = 8
        if self.rect.top > HEIGHT:
            self.speedy = -8
        if self.rect.bottom < 0:
            self.speedy = 8


class GoalIcon(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        icon_text = pygame.image.load(path.join(img_dir, 'goool_icon.png'))  # Define imagem do Player
        self.image = icon_text  # Coloca imagem do Player
        self.image.set_colorkey(BLACK)  # Deixa Transparente

        self.rect = self.image.get_rect()  # Obtem detalhes da posição
        self.rect.x = 0
        self.rect.y = 0
        self.speedx = 0
        self.reset()

    def reset(self):
        self.rect.x = 0  # Posiciona no centro em x
        self.rect.y = 180  # Posiciona objeto no centro em y
        self.speedx = 15

    def update(self):
        self.rect.x += self.speedx


pygame.init()
pygame.mixer.init()

# Tamanho da tela.
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Nome do jogo
pygame.display.set_caption("FutPong")

# Variável para o ajuste de velocidade
clock = pygame.time.Clock()

pygame.mixer_music.load(path.join(snd_dir, 'Skank-É uma Partida de Futebol.mp3'))
pygame.mixer_music.set_volume(1)
goal_sound = pygame.mixer.Sound(path.join(snd_dir, 'Goal Sound.wav'))

score_player1 = 0
score_player2 = 0

background1 = pygame.image.load(path.join(img_dir, 'intro.png')).convert()
background1_rect = background1.get_rect()
background2 = pygame.image.load(path.join(img_dir, 'campo.jpg')).convert()
background2_rect = background2.get_rect()
background3_1 = pygame.image.load(path.join(img_dir, 'vp1.png')).convert()
background3_1_rect = background2.get_rect()
background3_2 = pygame.image.load(path.join(img_dir, 'vp2.png')).convert()
background3_2_rect = background2.get_rect()

# Coloca jogadores no jogo
all_sprites = pygame.sprite.Group()
player1 = Players("esquerda")
player2 = Players("direita")
ball = Ball()
goal_icon = GoalIcon()

estado = 1

connection, address = serversocket.accept()

try:
    pygame.mixer.music.play(loops=-1)  # Coloca música no jogo
    running = True

    while running:

        clock.tick(FPS)

        if estado == 1:  # inicio do jogo
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    running = False
                elif evento.type == pygame.KEYUP:
                    if evento.key == pygame.K_SPACE:
                        estado = 1.5

        elif estado == 1.5:  # jogo em si
            all_sprites.add(player1)
            all_sprites.add(player2)
            all_sprites.add(ball)
            estado = 2

        elif estado == 2:  # jogo em si
            buf = connection.recv(12) #########################
            buf = str(buf)
            j1, j2 = conversor_buffer(buf)
            player1.rect.y = j1
            player2.rect.y = j2
            print(j1, j2)
            buf = 0 ######################################
            all_sprites.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            if player1.rect.colliderect(ball):
                ball.speedx = random.randrange(15, 25)
                ball.speedy = random.randrange(-25, 25)

            if player2.rect.colliderect(ball):
                ball.speedx = random.randrange(-25, -15)
                ball.speedy = random.randrange(-25, 25)

            # Detect gol from player 1
            if ball.rect.x < 85 and 138 < ball.rect.y < 509:
                all_sprites.add(goal_icon)
                goal_icon.reset()
                score_player1 += 1
                goal_sound.play()
                clock.tick(100)
                ball.reset()

            # Detect gol from player 2
            if ball.rect.x > 1024 and 142 < ball.rect.y < 514:
                all_sprites.add(goal_icon)
                goal_icon.reset()
                goal_sound.play()
                score_player2 += 1
                clock.tick(100)
                ball.reset()

            # colidir a bola com a trave e a linha de fundo
            if 125 <= ball.rect.x <= 133 and 0 <= ball.rect.y <= 137:
                ball.speedx = -ball.speedx
            if 125 <= ball.rect.x <= 133 and 515 <= ball.rect.y <= 654:
                ball.speedx = -ball.speedx

            if 1014 <= ball.rect.x <= 1025 and 0 <= ball.rect.y <= 141:
                ball.speedx = -ball.speedx
            if 1014 <= ball.rect.x <= 1025 and 515 <= ball.rect.y <= 654:
                ball.speedx = -ball.speedx

                pygame.display.flip()

            if score_player1 == 100:
                estado = 3.1
            elif score_player2 == 100:
                estado = 3.2

        elif estado == 3.1 or estado == 3.2:
            for e31 in pygame.event.get():
                if e31.type == pygame.QUIT:
                    running = False
                elif e31 == pygame.KEYDOWN:
                    estado = 1

        # A cada loop, redesenha o fundo e os sprites
        if estado == 1:
            screen.fill(BLACK)
            screen.blit(background1, background1_rect)

        elif estado == 2:
            screen.fill(BLACK)
            screen.blit(background2, background2_rect)
            all_sprites.draw(screen)
            draw_text(screen, str(score_player2), 60, 65, 20)
            draw_text(screen, str(score_player1), 60, 1085, 25)
        
        elif estado == 3.1:
            screen.fill(BLACK)
            screen.blit(background3_1, background3_1_rect)

        elif estado == 3.2:
            screen.fill(BLACK)
            screen.blit(background3_2, background3_2_rect)

        # Depois de desenhar tudo, inverte o display.
        pygame.display.flip()

finally:
    pygame.quit()
