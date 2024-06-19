import pygame
import sys
import os
import database
from img import images as img
from store import Inventario as inv
from store import Objetos as obj

pygame.init()

l=open('labirinto.txt')
lab=[]
for x in l:
    linha=[]
    for i in x.strip():
        linha.append(int(i))
    lab.append(linha)
l.close()

screen = pygame.display.set_mode((1920, 1011))

x, y = screen.get_size()   


GRID_SIZE = 48
pygame.display.set_caption("Os Labirintos da Unicamp")

player_img = pygame.transform.scale(img.baixo_img,(28,40))
player_rect=player_img.get_rect()
player_rect.center = (1, 1)

#Parâmtros do pygame
GRID_SIZE = 48
clock = pygame.time.Clock()

#Tudo da bomba
bomba_rectp=pygame.Rect(0,0,GRID_SIZE,GRID_SIZE)
bomba_rectg=pygame.Rect(0,0,150,150)
bomba_anim=False
bombas=[]

#Criação da lista Paredes
paredes=[]
cont_y=1
for i in lab:
    cont_x=0
    for j in i:
        if j==0:
            pass
        else:
            paredes.append(pygame.Rect(cont_x,cont_y,GRID_SIZE,GRID_SIZE))
        cont_x+=GRID_SIZE
    cont_y+=GRID_SIZE
tempo=0
tempo_morte=0
morte=False
menos=False

###DATABASE
database.init_db()

vidas=[1,1,1]
#Inventário
inventario=database.add_inventory(0)

print(inventario.status)


running = True
while running:
    #Fundo
    screen.blit(img.fundo_img, img.fundo_rect)

    player_rect_atual =player_rect.copy()
    #Tempo
    dt= clock.tick()
    clock.tick(100)

    #Desenho do grid
    for i in range(0,x,GRID_SIZE):
        pygame.draw.rect(screen, (128, 128, 128), pygame.Rect(i, 0, 1, y))
    for i in range(0,y,GRID_SIZE):
        pygame.draw.rect(screen, (128, 128, 128), pygame.Rect(0, i, x, 1))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if inventario.status==0:
                if event.key == pygame.K_LEFT:
                    player_img = pygame.transform.scale(img.esquerda_img,(28,40))
                    player_rect[0] -= GRID_SIZE
                elif event.key == pygame.K_RIGHT:
                    player_img = pygame.transform.scale(img.direita_img,(28,40))
                    player_rect[0] += GRID_SIZE
                elif event.key == pygame.K_UP:
                    player_img = pygame.transform.scale(img.cima_img,(28,40))
                    player_rect[1] -= GRID_SIZE
                elif event.key == pygame.K_DOWN:
                    player_img = pygame.transform.scale(img.baixo_img,(28,40))
                    player_rect[1] += GRID_SIZE
            if event.key == pygame.K_ESCAPE:
                running=False
            elif event.key == pygame.K_b and not bomba_anim:
                bomba_rectp.center, bomba_rectg.center=player_rect.center,player_rect.center
                bomba_anim=True
            elif event.key == pygame.K_i:
                if inventario.status==0:
                    inventario._status=1
                else:
                    inventario._status=0
            


    if bomba_anim:
        tempo+=dt
        screen.blit(img.bomba_img, bomba_rectp)
        bombas.append(pygame.Rect(bomba_rectp))
        if tempo>1000:
            bombas.clear()
            screen.blit(img.explosao_img, bomba_rectg)
            for k in range(5):
                for i in paredes:
                    if bomba_rectg.colliderect(i):
                        y_lab=i[0]//GRID_SIZE
                        x_lab=i[1]//GRID_SIZE
                        lab[x_lab][y_lab]=0
                        paredes.remove(i)
                        if 0 in vidas:
                            vidas.remove(0)
                            vidas.append(1)
                        else:
                            vidas.append(1)
                        vidas.sort(reverse=True)
                if bomba_rectg.colliderect(player_rect):
                    if menos==False:
                        menos=True
                        print(vidas.count(1))
                        if vidas.count(1)!=0:
                            vidas.remove(1)
                            vidas.append(0)
                            vidas.sort(reverse=True)
                            player_img = pygame.transform.scale(img.baixo_img,(28,40))
                            morte=True

            if tempo>1100:
                bomba_anim=False                    
                tempo=0
                menos=False
                    
    if morte:
        tempo_morte+=dt
        player_img = pygame.transform.scale(img.morte_img,(100,100))
        if tempo_morte>1000:
            player_rect.center=(1,1)
            tempo_morte=0
            morte=False
            player_img = pygame.transform.scale(img.baixo_img,(28,40))


    #Encontrou a saída
    if player_rect.colliderect(img.saida_rect):
        running=False

    #Colisão com as paredes
    for p in paredes:
        screen.blit(img.parede_img, p)
        if player_rect.colliderect(p):
            player_rect[0] =player_rect_atual[0]
            player_rect[1] =player_rect_atual[1]
    #Colisao com a bomba antes de explodir
    for b in bombas:
        screen.blit(img.bomba_img, b)
        if player_rect.colliderect(b):
            player_rect[0] =player_rect_atual[0]
            player_rect[1] =player_rect_atual[1]

    #Limites de onde o jogador pode andar
    player_rect[0] = max(9, min(player_rect[0], x-GRID_SIZE))
    player_rect[1] = max(5, min(player_rect[1], y-GRID_SIZE))

    #Desenho de tanto a saída como o jogador
    screen.blit(img.saida_img, img.saida_rect)
    screen.blit(player_img, player_rect)

    pos_vidas=0
    for v in vidas:
        if v==0:
            screen.blit(img.coracao_vazio_img, pygame.Rect(10+pos_vidas, 10, 30, 30))
        else:
            screen.blit(img.coracao_cheio_img, pygame.Rect(10+pos_vidas, 10, 30, 30))
        pos_vidas+=40

    if 1 not in vidas:
        running=False

    #Atualizar a tela
    pygame.display.flip()

#Atualização do labirinto

open('labirinto.txt','w').close()
with open('labirinto.txt','a') as l:
    for i in lab:
        for j in i:
            l.write(str(j))
        l.write('\n')

pygame.quit()
sys.exit()
