import os
import random
import math
import pygame
from os import listdir
from os.path import isfile, join

pygame.init()

pygame.display.set_caption("Python Platformer Tutorial Project")

BG_COLOR = (255,255,255)
WIDTH,HEIGHT = 1280, 720
FPS = 60

window = pygame.display.set_mode((WIDTH, HEIGHT))

def get_background(bg_name):
    image = pygame.image.load(join("assets","Background",bg_name))
    _, _, width, height = image.get_rect()
    tiles = []

    for i in range(WIDTH//width + 1):
        for j in range(HEIGHT//height + 1):
            pos = (i * width, j * height)
            tiles.append(pos)

    return tiles,image

def draw(window,background, bg_image):
    for tile in background:
        window.blit(bg_image, tile)

    pygame.display.update()

def main(window):
    time = pygame.time.Clock()
    background,bg_image = get_background("Brown.png")

    run = True

    while run:
        time.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        draw(window,background,bg_image)

    pygame.quit()
    quit()
        
if __name__ == "__main__":
    main(window)