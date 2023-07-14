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
PLAYER_SPEED = 10
JUMP_HEIGHT = 5
FPS = 60

window = pygame.display.set_mode((WIDTH, HEIGHT))

def handle_movement(player):
    keys = pygame.key.get_pressed()

    player.x_vel = 0
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        player.move_left(PLAYER_SPEED)
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        player.move_right(PLAYER_SPEED)
    #if keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]:
    #    player.jump(JUMP_HEIGHT)

def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]

def load_spritesheet(dir1, dir2, width, height, direction = False):
    path = join("assets", dir1, dir2)
    images = [f for f in listdir(path) if isfile(join(path,f))]

    all_sprites = {}
    for image in images:
        spritesheet = pygame.image.load(join(path,image)).convert_alpha()

        sprites = []
        for i in range(spritesheet.get_width()// width ):
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(spritesheet, (0,0), rect)
            sprites.append(pygame.transform.scale2x(surface))

        if direction:
            all_sprites[image.replace(".png", "") + "_right"] = sprites
            all_sprites[image.replace(".png", "") + "_left"] = flip(sprites)
        else:
            all_sprites[image.replace(".png", "")] = sprites

    return all_sprites

class Player(pygame.sprite.Sprite):
    COLOR = (255,0,0)
    GRAVITY = 10
    SPRITES = load_spritesheet("MainCharacters", "PinkMan", 32, 32, True)
    ANIMATION_DELAY = 2

    def __init__(self, pos_x, pos_y, width, height):
        self.rect = pygame.Rect(pos_x, pos_y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.fall_counter = 0
        self.grounded = True

    def move(self, displacement_x, displacement_y):
        self.rect.x += displacement_x
        self.rect.y += displacement_y

    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def jump(self, vel):
        self.y_vel = vel,
        self.animation_count = 0
        self.grounded = False

    def loop(self, fps):
#        self.y_vel += min(1, (self.fall_counter/fps) * self.GRAVITY)
        self.move(self.x_vel, self.y_vel)

#        if self.grounded == False:
        self.fall_counter += 1
        self.update_sprite()
        
#        if self.rect.y == self.startY:
#            self.grounded = True

    def update_sprite(self):
        spritesheet = "idle"
        if self.x_vel != 0:
            spritesheet = "run"

        spritesheet_name = spritesheet + "_" + self.direction
        sprites = self.SPRITES[spritesheet_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1

    def draw(self, window):
        window.blit(self.sprite, (self.rect.x, self.rect.y))


def get_background(bg_name):
    image = pygame.image.load(join("assets","Background",bg_name))
    _, _, width, height = image.get_rect()
    tiles = []

    for i in range(WIDTH//width + 1):
        for j in range(HEIGHT//height + 1):
            pos = (i * width, j * height)
            tiles.append(pos)

    return tiles,image

def draw(window,background, bg_image, player):
    for tile in background:
        window.blit(bg_image, tile)

    player.draw(window)

    pygame.display.update()

def main(window):
    time = pygame.time.Clock()
    background,bg_image = get_background("Brown.png")

    player = Player(100, 100, 50, 50)

    run = True

    while run:
        time.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        handle_movement(player)
        player.loop(FPS)
        draw(window,background,bg_image, player)

    pygame.quit()
    quit()
        
if __name__ == "__main__":
    main(window)