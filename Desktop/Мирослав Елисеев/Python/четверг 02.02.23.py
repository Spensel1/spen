import pygame
pygame.init()
W=400
H=600
sc=pygame.display.set_mode((W,H))
pygame.display.set_caption('SuperPuperMegaGiperGame')
RED=(255,0,0)
GREEN=(0,255,0)
BLACK=(0,0,0)
WHITE=(255,255,255)
FPS=60
clock=pygame.time.Clock()
x=200
y=550
x1=200
y1=50
speed=5
while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            exit()
        '''elif event.type==pygame.KEYDOWN:
            if event.key==pygame.K_a:
                x-=speed
            elif event.key==pygame.K_d:
                x+=speed'''
    keys=pygame.key.get_pressed()
    if keys[pygame.K_a]:
        x-=speed
    elif keys[pygame.K_d]:
        x+=speed
    sc.fill(BLACK)
    #pygame.draw.lines(sc,GREEN,True,[(x-15,y+10),(x,y-10),(x+15,y+10)],5)
    pygame.draw.polygon(sc, GREEN,[[x-15,y+10],[x,y-10],[x+15,y+10]])
    pygame.draw.circle(sc,WHITE,(x1,y1),15)
    pi=3.14
    pygame.draw.arc(sc,BLACK,(x1-10,y1-8,20,20),pi,2*pi,2)
    pygame.draw.ellipse(sc,BLACK,(x1-6,y1-7,3,6))
    pygame.draw.ellipse(sc,BLACK,(x1+3,y1-7,3,6))












    pygame.display.update()
    clock.tick(FPS)






