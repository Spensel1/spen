import pygame
pygame.init()
W,H=800,600
sc = pygame.display.set_mode((800,600))
pygame.display.set_caption("MyFirstSuperGame")
WHITE=(255,255,255)
BLACK=(0,0,0)
RED=(255,0,0)
BLUE=(0,0,255)
YELLOW=(255,255,0)

pygame.draw.rect(sc,BLUE,(10,10,50,100),5)

pygame.display.update()
pygame.draw.line(sc,BLACK,(x,yx))
pygame.draw.circle(sc,YELLOW,(x,y),40)

pygame.display.update()















while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            exit