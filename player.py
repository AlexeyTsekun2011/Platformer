import pygame as pg
import pytmx
from constants import *
class Player(pg.sprite.Sprite):
    def __init__(self, map_width, map_height):
        super(Player, self).__init__()

        self.load_animations()
        self.current_animation = self.idle_animation_right
        self.current_image = 0
        self.image = self.current_animation[self.current_image]
        self.speed = 5
        self.rect = self.image.get_rect()
        self.rect.center = (120, 500)  # Начальное положение персонажа

        # Начальная скорость и гравитация
        self.velocity_x = 0
        self.velocity_y = 0
        self.gravity = 1
        self.is_jumping = False
        self.map_width = map_width * TILE_SCALE
        self.map_height = map_height * TILE_SCALE

        self.timer = pg.time.get_ticks()
        self.interval = 300

        self.hp = 10
        self.damage_timer = pg.time.get_ticks()
        self.damage_interval = 500

    def get_damage(self):
        if pg.time.get_ticks() - self.damage_timer > self.damage_interval:
            self.hp -= 1
            self.damage_timer = pg.time.get_ticks()

    def update(self, platforms):
        keys = pg.key.get_pressed()

        if keys[pg.K_w] and not self.is_jumping:
            self.jump()

        if keys[pg.K_a]:
            if self.current_animation != self.running_animation_left:
                self.current_animation = self.running_animation_left
                self.current_image = 0
            self.velocity_x = -self.speed

        elif keys[pg.K_d]:
            if self.current_animation != self.running_animation_right:
                self.current_animation = self.running_animation_right
                self.current_image = 0
            self.velocity_x = self.speed
        else:
            if self.current_animation == self.running_animation_right:
                self.current_animation = self.idle_animation_right
                self.current_image = 0
            elif self.current_animation == self.running_animation_left:
                self.current_animation = self.idle_animation_left
                self.current_image = 0

            self.velocity_x = 0
        # worlds limits
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

    def jump(self):
        self.velocity_y = -12 * TILE_SCALE
        self.is_jumping = True

    def load_animations(self):
        tile_size = 32
        num_images = 2
        spritesheet = pg.image.load("Sprite pack 4/1 - Agent_Mike_Idle (32 x 32).png")
        self.idle_animation_right = []
        for i in range(num_images):
            x = i * tile_size
            y = 0
            rect = pg.Rect(x, y, tile_size, tile_size)
            image = spritesheet.subsurface(rect)
            image = pg.transform.scale_by(image, 3.5)  # увеличение картинки в 2 раза
            self.idle_animation_right.append(image)

        self.idle_animation_left = [pg.transform.flip(image, True, False)
                                    for image in self.idle_animation_right]

        self.running_animation_right = []
        num_images = 6
        spritesheet = pg.image.load("Sprite pack 4/1 - Agent_Mike_Running (32 x 32).png")
        for i in range(num_images):
            x = i * tile_size
            y = 0
            rect = pg.Rect(x, y, tile_size, tile_size)
            image = spritesheet.subsurface(rect)
            image = pg.transform.scale_by(image, 3.5)
            self.running_animation_right.append(image)

        self.running_animation_left = [pg.transform.flip(image, True, False)
                                       for image in self.running_animation_right]

