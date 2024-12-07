import pygame

# задание начальных параметров
pygame.init()
W=600
H=400

sc=pygame.display.set_mode((W,H))
pygame.display.set_caption('MyFirstSuperGame')
WHITE=(255,255,255)
BLUE=(0,0,255)
GREEN=(0,255,0)
RED=(255,0,0)
BLACK=(0,0,0)
FPS=60
clock=pygame.time.Clock()
x=W//2
y=H//2
speed=3
while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            exit()
        '''elif event.type==pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:
                x-=speed
            elif event.key==pygame.K_RIGHT:
                x+=speed
            elif event.key == pygame.K_UP:
                y -= speed
            elif event.key == pygame.K_DOWN:
                y += speed'''
    keys=pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        x-=speed
    elif keys[pygame.K_RIGHT]:
        x+=speed
    elif keys[pygame.K_UP]:
        y-=speed
    elif keys[pygame.K_DOWN]:
        y+=speed
    sc.fill(BLACK)
    pygame.draw.rect(sc, RED, (x,y,10,10))
    pygame.display.update()
    clock.tick(FPS)
