import pygame
import os
from random import randint
pygame.init()

WIN_WIDTH = 700
WIN_HEIGHT = 500 
FPS = 40
BLACK = (70, 70, 70)
RED = (240, 0, 0)
GREEN = (0, 240, 0)

def file_path(file_name):
    folder_path = os.path.abspath(__file__ + "/..")
    path = os.path.join(folder_path, file_name)
    return path

image_background = pygame.image.load(file_path("background.png"))
image_background = pygame.transform.scale(image_background, (WIN_WIDTH, WIN_HEIGHT))

pygame.mixer.music.load(file_path("music.wav"))
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play()

window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
clock = pygame.time.Clock()

class Gamesprite(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, img, speed):
        super().__init__()
        self.image = pygame.image.load(file_path(img))
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(Gamesprite):
    def __init__(self, x, y, width, height, img, speed):
        super().__init__(x, y, width, height, img, speed)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_d]:
            self.rect.x += self.speed
    
    def fire(self):
        bullet = Bullet(self.rect.centerx, self.rect.top, 10, 10, file_path("bullet.png"), 5)
        bullets.add(bullet)

class Bullet(Gamesprite):
    def __init__(self, x , y, width, height, img, speed):
        super().__init__(x, y, width, height, img, speed)
   
    def update(self):
        global score_lose
        self.rect.y -= self.speed
        if self.rect.bottom <= 0:
            self.kill()

class Enemy(Gamesprite):
    def __init__(self, x , y, width, height, img, speed):
        super().__init__(x, y, width, height, img, speed)
    
    def update(self):
        global score_lose
        self.rect.y += self.speed
        if self.rect.y > WIN_HEIGHT:
            self.rect.x = randint(0, WIN_WIDTH - 70)
            score_lose += 1
            self.rect.y = 0




enemys = pygame.sprite.Group()
for i in range(5):
    enemy = Enemy(randint(0, WIN_WIDTH - 70), 0, 70, 70, file_path("enemy.png"), randint(1,4))
    enemys.add(enemy)

bullets = pygame.sprite.Group()


player = Player(300, 400, 70, 70, "player.png", 5)

score_lose = 0
score_destroy = 0

font = pygame.font.SysFont("verdana", 30)

play = True
game = True
while game == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.fire()

    if play == True:
        window.blit(image_background, (0, 0))
        
        txt_lose = font.render("lost: " + str(score_lose), True, BLACK)
        txt_destroy = font.render("destroyed: " + str(score_destroy), True, BLACK)
        window.blit(txt_lose, (50, 50))
        window.blit(txt_destroy, (50, 100))


        player.reset()
        player.update()

        enemys.draw(window)
        enemys.update()

        bullets.draw(window)
        bullets.update()

        enemysandbullets = pygame.sprite.groupcollide(enemys, bullets, False, True)
        if enemysandbullets:
            for enemy in enemysandbullets:
                score_destroy += 1
                enemy.rect.x = randint(0, WIN_WIDTH - 70)
                enemy.rect.y = 0
        
        if score_lose >= 5 or pygame.sprite.spritecollide(player, enemys, False):
            play = False
            font2 = pygame.font.SysFont("arial", 50, 1)
            txt_gameover = font2.render("you lost", True, RED)
            window.blit(txt_gameover, (250, 200))
        
        if score_destroy >= 10:
            play = False
            font3 = pygame.font.SysFont("arial", 50, 1)
            txt_gamewin = font3.render("you win", True, GREEN)
            window.blit(txt_gamewin, (250, 200))
        


    clock.tick(FPS)
    pygame.display.update()