# -*-coding:utf-8-*-
import pygame, sys
import random

class Ball(pygame.sprite.Sprite):
    def __init__(self, image_file, location, speed=[0,0]):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        self.speed = speed

    def move(self, splat):
        self.rect = self.rect.move(self.speed)
        if self.rect.left < 0 or self.rect.right > screen.get_width() :
            self.speed[0] = -self.speed[0]
            splat.play()
        if self.rect.top <= 40 :
            self.speed[1] = -self.speed[1]
            splat.play()

class Brick(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        x, y = location
        self.rect.left = x * 50
        self.rect.top = 80 + y * 25

class Plate(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

def animate(ball, bGroup, plate, splat, splat2):
    ball.move(splat2)
    leftp = (ball.rect.left, ball.rect.top+5)
    rightp = (ball.rect.right, ball.rect.top+5)
    topp = (ball.rect.left+5, ball.rect.top)
    bottomp = (ball.rect.left+5, ball.rect.bottom)
    for brick in bGroup:
        global score
        if leftp[0] < brick.rect.right and leftp[0] > brick.rect.left:
            if leftp[1] > brick.rect.top and leftp[1] < brick.rect.bottom:
                ball.speed[0] = 2
                bGroup.remove(brick)
                score += 1
                splat.play()
                break
        if rightp[0] > brick.rect.left and rightp[0] < brick.rect.right:
            if rightp[1] > brick.rect.top and rightp[1] < brick.rect.bottom:
                bGroup.remove(brick)
                score += 1
                ball.speed[0] = -2
                splat.play()
                break
        if topp[1] < brick.rect.bottom and topp[1] > brick.rect.top:
            if topp[0] > brick.rect.left and topp[0] < brick.rect.right:
                ball.speed[1] = 3
                bGroup.remove(brick)
                score += 1
                splat.play()
                break
        if bottomp[1] > brick.rect.top and bottomp[1] < brick.rect.bottom:
            if bottomp[0] > brick.rect.left and bottomp[0] < brick.rect.right:
                ball.speed[1] = -3
                bGroup.remove(brick)
                score += 1
                splat.play()
                break

    if bottomp[1] > plate.rect.top and bottomp[0] > plate.rect.left and bottomp[0] < plate.rect.right:
        ball.speed[1] = -3
        splat2.play()
    if leftp[0] < plate.rect.right and leftp[0] > plate.rect.left:
        if leftp[1] > plate.rect.top and leftp[1] < plate.rect.bottom:
            splat2.play()
            ball.speed[0] = 2
    if rightp[0] > plate.rect.left and rightp[0] < plate.rect.left:
        if rightp[1] > plate.rect.top and rightp[1] < plate.rect.bottom:
            splat2.play()
            ball.speed[0] = -2

def fonts(text, size, x, y):
    font = pygame.font.Font(None, size)
    content = font.render(text, 1,(0,0,0))
    textpos = [x, y]
    screen.blit(content, textpos)
    return content

def listInit():
    listSet = set([])
    while len(listSet) < 50:
        x = random.randint(0,8)
        y = random.randint(0,8)
        listSet.add((x,y))
    group = pygame.sprite.Group()
    for i in listSet:
        brick = Brick('brick.png', i)
        group.add(brick)
    return group
pygame.init()
screen = pygame.display.set_mode([450,600], 0, 32)
listSet = listInit()

plate = Plate('plate.png', (140,570))

pygame.mixer.music.load('th_9 .mp3')
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)
splat = pygame.mixer.Sound('hit_paddle.wav')
splat.set_volume(0.5)
splat2 = pygame.mixer.Sound('hit_wall.wav')
splat2.set_volume(0.3)
splat3 = pygame.mixer.Sound('splat.wav')
splat3.set_volume(0.5)
splat4 = pygame.mixer.Sound('new_life.wav')
splat4.set_volume(0.5)

group = listInit()
ball = []
for i in range(3):
    ball.append(Ball('ball.png',(screen.get_width()-(i+1)*20, 20) ))

runball = 0
global score
score = 0
ball[runball].speed = [-2, -3]
ball[runball].rect.left, ball[runball].rect.top = (195,550)
times = 20

page = 0
while True:
    if page == 0:
        screen.fill([255,255,255])
        pygame.draw.rect(screen, [200, 200, 200], [93, 300, 260, 40], 0)
        fonts('Game Start', 64, 100, 300)
        pygame.draw.rect(screen, [200, 200, 200], [103, 380, 240, 40], 0)
        fonts('Game Exit', 64, 110, 380)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[0] > 93 and event.pos[0] < 353:
                    if event.pos[1]> 300 and event.pos[1] < 340:
                        page = 1
                        pygame.mixer.music.stop()
                        pygame.mixer.music.load('TEBASAKI.mp3')
                        pygame.mixer.music.set_volume(0.3)
                        pygame.mixer.music.play()
                if event.pos[0] > 103 and event.pos[0] < 343:
                    if event.pos[1]> 380 and event.pos[1] < 420:
                        sys.exit()

    elif page == 1:
        
        screen.fill([255,255,255])
        for brick in group:
            screen.blit(brick.image, brick.rect)
        screen.blit(plate.image, plate.rect)
        for b in ball:
            screen.blit(b.image, b.rect)
        fonts('Score:  %s:%s' % (score,len(group)), 22, 20,20)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEMOTION:
                plate.rect.centerx = event.pos[0]
        animate(ball[runball], group, plate, splat, splat2)
        pygame.time.delay(times)
        if ball[runball].rect.top > screen.get_rect().bottom:
            splat3.play()
            ball[runball].speed = (0,0)
            runball += 1
            if runball > 2 :
                page = 2
                pygame.mixer.music.stop()
                pygame.mixer.music.load('th_9 .mp3')
                pygame.mixer.music.set_volume(0.3)
                pygame.mixer.music.play()
                continue
            ball[runball].speed = [-2, -3]
            ball[runball].rect.left, ball[runball].rect.top = (195,550)
            pygame.time.delay(2000)
            splat4.play()
        if len(group) < 1:
            screen.fill([255,255,255])
            fonts('pass the checkpoint', 40, 90,250)
            fonts('next level', 40, 160,300)
            pygame.display.flip()
            pygame.time.delay(2000)
            ball[runball].speed = [-2, -3]
            ball[runball].rect.left, ball[runball].rect.top = (195,550)
            group = listInit()
            times -= 1
    elif page == 2:
        screen.fill([255,255,255])
        fonts('Score:', 40, 100, 200)
        fonts(str(score),40, 200,200)
        pygame.draw.rect(screen, [200, 200, 200], [93, 300, 260, 40], 0)
        fonts('Game Start', 64, 100, 300)
        pygame.draw.rect(screen, [200, 200, 200], [103, 380, 240, 40], 0)
        fonts('Game Exit', 64, 110, 380)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[0] > 93 and event.pos[0] < 353:
                    if event.pos[1]> 300 and event.pos[1] < 340:
                        page = 1
                        pygame.mixer.music.stop()
                        pygame.mixer.music.load('TEBASAKI.mp3')
                        pygame.mixer.music.set_volume(0.3)
                        pygame.mixer.music.play()
                        ball = []
                        for i in range(3):
                            ball.append(Ball('ball.png',(screen.get_width()-(i+1)*20, 20) ))
                        runball = 0
                        ball[runball].speed = [-2, -3]
                        ball[runball].rect.left, ball[runball].rect.top = (195,550)
                        group = listInit()
                        score = 0
                        
                        
                        
                if event.pos[0] > 103 and event.pos[0] < 343:
                    if event.pos[1]> 380 and event.pos[1] < 420:
                        sys.exit()
    elif page == 3:
        screen.fill([255,255,255])
        fonts('pass the checkpoint', 40, 90,250)
        fonts('next level', 40, 160,300)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        
