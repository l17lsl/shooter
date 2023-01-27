import pygame
import os
pygame.init()

WIN_WIDTH = 700
WIN_HEIGHT = 500 
FPS = 40

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

play = True
game = True
while game == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False

    if play == True:
        window.blit(image_background, (0, 0))

    clock.tick(FPS)
    pygame.display.update()