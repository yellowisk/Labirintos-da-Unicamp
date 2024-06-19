import pygame
import os

cima_img = pygame.image.load(os.path.join("img","cima.png"))
baixo_img = pygame.image.load(os.path.join("img","baixo.png"))
direita_img = pygame.image.load(os.path.join("img","direita.png"))
esquerda_img = pygame.image.load(os.path.join("img","esquerda.png"))
morte_img= pygame.image.load(os.path.join("img","morte.png"))

GRID_SIZE = 48

saida_img=pygame.image.load(os.path.join("img","jogador2.gif"))
parede_img=pygame.image.load(os.path.join("img","parede.jpeg"))
parede_img = pygame.transform.scale(parede_img,(GRID_SIZE,GRID_SIZE))

bomba_img=pygame.image.load(os.path.join("img","bomba.png"))
explosao_img=pygame.image.load(os.path.join("img","explosion.gif"))
bomba_img = pygame.transform.scale(bomba_img,(GRID_SIZE,GRID_SIZE))
explosao_img = pygame.transform.scale(explosao_img,(150,150))
fundo_img=pygame.image.load(os.path.join("img","fundo.png"))
fundo_img = pygame.transform.scale(fundo_img,(1920,1011))
fundo_rect=fundo_img.get_rect()
fundo_rect.center=(960,505)

player_img = pygame.transform.scale(baixo_img,(28,40))
player_rect=player_img.get_rect()
player_rect.center = (1, 1)

saida_rect=saida_img.get_rect()
saida_rect.center=(1890,42)

coracao_cheio_img=pygame.image.load(os.path.join("img","coracao_cheio.png"))
coracao_vazio_img=pygame.image.load(os.path.join("img","coracao_vazio.png"))
coracao_vazio_img = pygame.transform.scale(coracao_vazio_img,(60,34))
coracao_cheio_img = pygame.transform.scale(coracao_cheio_img,(60,34))

