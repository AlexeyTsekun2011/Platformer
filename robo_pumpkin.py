import pygame as pg
from constants import *


class RoboPumpkin(pg.sprite.Sprite):
    def __init__(self, map_width, map_height,x,y):
        super(RoboPumpkin,self).__init__()

        self.load_animations()
        self.current_animation = self.running_animation_right
        self.current_image = 0
        self.image = self.current_animation[self.current_image]

        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x,y)  # Начальное положение персонажа

        self.left_edge = self.rect.left - 16 * TILE_SCALE
        self.right_edge = self.rect.right + 16 * TILE_SCALE

        self.direction = "left"

        # Начальная скорость и гравитация
        self.velocity_x = 0
        self.velocity_y = 0
        self.gravity = 2
        self.is_jumping = False
        self.map_width = map_width * TILE_SCALE
        self.map_height = map_height * TILE_SCALE

        self.timer = pg.time.get_ticks()
        self.interval = 200

    def load_animations(self):
        tile_size = 16
        # spritesheet = pg.image.load("Sprite pack 2/4 - Robo Pumpkin/Standing (16 x 16).png")
        # self.idle_animation_right = []
        #
        #
        # self.idle_animation_left = [pg.transform.flip(image, True, False)
        #                             for image in self.idle_animation_right]

        self.running_animation_left = []
        num_images = 2
        spritesheet = pg.image.load("Sprite Pack 2/4 - Robo Pumpkin/Walking (16 x 16).png")
        for i in range(num_images):
            x = i * tile_size
            y = 0
            rect = pg.Rect(x, y, tile_size, tile_size)
            image = spritesheet.subsurface(rect)
            image = pg.transform.scale_by(image, 3.5)
            self.running_animation_left.append(image)

        self.running_animation_right = [pg.transform.flip(image, True, False)
                                       for image in self.running_animation_left]

    def update(self, platforms):
        if self.direction == "right":
            self.current_animation = self.running_animation_right
            self.velocity_x = 2.25
            if self.rect.right >= self.right_edge:
                self.direction = "left"
        elif self.direction == "left":
            self.velocity_x = -2.25
            self.current_animation = self.running_animation_left
            if self.rect.left <= self.left_edge:
                self.direction = "right"
                self.current_animation = self.running_animation_right
        new_x = self.rect.x + self.velocity_x
        if 0 <= new_x <= self.map_width - self.rect.width:
            self.rect.x = new_x

        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y
        # Проверка на столкновение с платформой во время прыжка
        for platform in platforms:
            if platform.rect.collidepoint(self.rect.midbottom):
                self.rect.bottom = platform.rect.top
                self.velocity_y = 0
                self.is_jumping = False

            if platform.rect.collidepoint(self.rect.midtop):
                self.rect.top = platform.rect.bottom
                self.velocity_y = 0

            if platform.rect.collidepoint(self.rect.midright):
                self.rect.right = platform.rect.left

            if platform.rect.collidepoint(self.rect.midleft):
                self.rect.left = platform.rect.right

        if pg.time.get_ticks() - self.timer > self.interval:
            self.current_image += 1
            if self.current_image >= len(self.current_animation):
                self.current_image = 0
            self.image = self.current_animation[self.current_image]
            self.timer = pg.time.get_ticks()


