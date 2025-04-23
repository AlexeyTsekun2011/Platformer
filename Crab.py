import pygame as pg
from constants import *

class Crab(pg.sprite.Sprite):
    def __init__(self, map_width, map_height,x,y):
        super(Crab, self).__init__()


        self.load_animations()
        self.current_animation = self.move_animation
        self.current_image = 0
        self.image = self.current_animation[self.current_image]

        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x,y)  # Начальное положение персонажа

        self.left_edge = self.rect.left - 16 * TILE_SCALE
        self.right_edge = self.rect.right + 16 * TILE_SCALE



        self.direction = "right"

        # Начальная скорость и гравитация
        self.velocity_x = 0
        self.velocity_y = 0
        self.gravity = 2
        self.is_jumping = False
        self.map_width = map_width * TILE_SCALE
        self.map_height = map_height * TILE_SCALE

        self.timer = pg.time.get_ticks()
        self.interval = 400

    def load_animations(self):
        self.move_animation = []
        image = pg.image.load("Sprite Pack 2/9 - Snip Snap Crab/Movement_(Flip_image_back_and_forth) (32 x 32).png")
        image = pg.transform.scale_by(image, 3.5)  # увеличение картинки в 2 раза
        self.move_animation.append(image)
        self.move_animation.append(pg.transform.flip(image,True,False))

    def update(self,platforms):
        if self.direction == "right":
            self.velocity_x = 3
            if self.rect.right >= self.right_edge:
                self.direction = "left"
        elif self.direction == "left":
            self.velocity_x = -3
            if self.rect.left <= self.left_edge:
                self.direction = "right"
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
