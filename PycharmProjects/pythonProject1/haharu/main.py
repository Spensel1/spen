import pygame


# задание начальных параметров
pygame.init()
W=600
H=400

sc=pygame.display.set_mode((W,H))
pygame.display.set_caption('MyFirstSuperGame')
WHITE=(255,255,255)
GREEN=(0,255,0)
BLACK=(0,0,0)
pygame.draw.rect(sc,WHITE,(10,10,50,100),1)
pygame.draw.line(sc,GREEN,(200,20),(350,20),1)
pygame.draw.lines(sc,RED,True,[(200,80),(250,80),(300,200)])
pygame.display.update()
input()