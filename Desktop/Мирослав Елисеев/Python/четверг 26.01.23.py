import pygame
pygame.init()
W=600
H=400
sc=pygame.display.set_mode((W,H))
pygame.display.set_caption('MyFirstSuperGame')
WHITE=(255,255,255)
GREEN=(0,255,0)
BLACK=(0,0,0)
RED=(255,0,0)
BLUE=(0,0,255)
pygame.draw.rect(sc,WHITE,(10,10,50,100),1)
pygame.draw.line(sc,GREEN,(200,20),(350,20),1)
pygame.draw.lines(sc,RED,True,[(200,80),(250,80),(300,200)])
pygame.draw.circle(sc,BLUE,(300,250),40)
pi=3.14
pygame.draw.arc(sc,RED,(450,30,50,150),pi,2*pi,5)
x_h=W//2
y_y=H-205
pygame.display.update()





















































































