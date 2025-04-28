import pygame as pg
import pytmx
from constants import *
from Crab import Crab
from robo_pumpkin import RoboPumpkin
from ball import Ball

# pip install pytmx
pg.init()
pg.mixer.init()
pg.mixer.music.load("sounds/music/02. Title Theme.mp3")
pg.mixer.music.play()
font = pg.font.Font(None, 72)
shoot = pg.mixer.Sound("sounds/sounds/163456__lemudcrab__pistol-shot.wav")
coin = pg.mixer.Sound("sounds/sounds/super-mario-coin-sound-effect.wav")


class Platform(pg.sprite.Sprite):
    def __init__(self, image, x, y, width, height):
        super().__init__()
        self.image = pg.transform.scale_by(image, TILE_SCALE)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SCALE
        self.rect.y = y * TILE_SCALE


class Portal(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.load_animation()
        self.current_image = 0
        self.image = self.animation[self.current_image]
        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SCALE
        self.rect.bottom = y * TILE_SCALE
        self.timer = pg.time.get_ticks()
        self.interval = 200

    def load_animation(self):
        num_images = 8
        tile_size = 64
        self.animation = []
        spritesheet = pg.image.load("Assets/portals/Green Portal Sprite Sheet.png")
        for i in range(num_images):
            x = i * tile_size
            y = 0
            rect = pg.Rect(x, y, tile_size, tile_size)
            image = spritesheet.subsurface(rect)
            image = pg.transform.scale_by(image, TILE_SCALE)  # увеличение картинки в 2 раза
            image = pg.transform.flip(image, True, False)
            self.animation.append(image)

    def update(self):
        if pg.time.get_ticks() - self.timer > self.interval:
            self.current_image += 1
            if self.current_image >= len(self.animation):
                self.current_image = 0
            self.image = self.animation[self.current_image]
            self.timer = pg.time.get_ticks()


class Coin(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.load_animation()
        self.current_image = 0
        self.image = self.animation[self.current_image]
        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SCALE
        self.rect.y = y * TILE_SCALE
        self.timer = pg.time.get_ticks()
        self.interval = 200

    def load_animation(self):
        num_images = 5
        tile_size = 16
        self.animation = []
        spritesheet = pg.image.load("Assets/Coin_Gems/MonedaD.png")
        for i in range(num_images):
            x = i * tile_size
            y = 0
            rect = pg.Rect(x, y, tile_size, tile_size)
            image = spritesheet.subsurface(rect)
            image = pg.transform.scale_by(image, TILE_SCALE)  # увеличение картинки в 2 раза
            self.animation.append(image)

    def update(self):
        if pg.time.get_ticks() - self.timer > self.interval:
            self.current_image += 1
            if self.current_image >= len(self.animation):
                self.current_image = 0
            self.image = self.animation[self.current_image]
            self.timer = pg.time.get_ticks()


class Player(pg.sprite.Sprite):
    def __init__(self, map_width, map_height):
        super(Player, self).__init__()

        self.load_animations()
        self.current_animation = self.idle_animation_right
        self.current_image = 0
        self.image = self.current_animation[self.current_image]

        self.rect = self.image.get_rect()
        self.rect.center = (120, 500)  # Начальное положение персонажа

        # Начальная скорость и гравитация
        self.velocity_x = 0
        self.velocity_y = 0
        self.gravity = 2
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
            self.hp -= 2
            self.damage_timer = pg.time.get_ticks()

    def update(self, platforms):
        keys = pg.key.get_pressed()

        if keys[pg.K_SPACE] and not self.is_jumping:
            self.jump()

        if keys[pg.K_a]:
            if self.current_animation != self.running_animation_left:
                self.current_animation = self.running_animation_left
                self.current_image = 0
            self.velocity_x = -5

        elif keys[pg.K_d]:
            if self.current_animation != self.running_animation_right:
                self.current_animation = self.running_animation_right
                self.current_image = 0
            self.velocity_x = 5
        else:
            if self.current_animation == self.running_animation_right:
                self.current_animation = self.idle_animation_right
                self.current_image = 0
            elif self.current_animation == self.running_animation_left:
                self.current_animation = self.idle_animation_left
                self.current_image = 0

            self.velocity_x = 0
        # Границы игрового мира
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
        self.velocity_y = -16 * TILE_SCALE
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


class Game:
    def __init__(self):
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption("Платформер")
        self.clock = pg.time.Clock()
        self.is_running = False
        self.level = 1

        self.setup()

    # noinspection PyAttributeOutsideInit
    def setup(self):
        self.mode = "game"

        background = pg.image.load("tilesetOpenGameBackground.png")
        self.background = pg.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.balls = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.portals = pg.sprite.Group()

        self.tmx_map = pytmx.load_pygame(f"level{self.level}.tmx")
        self.map_pixel_width = self.tmx_map.width * self.tmx_map.tilewidth * TILE_SCALE
        self.map_pixel_height = self.tmx_map.height * self.tmx_map.tileheight * TILE_SCALE

        self.player = Player(self.map_pixel_width, self.map_pixel_height)
        self.all_sprites.add(self.player)

        self.camera_x = 0
        self.camera_y = 0
        self.camera_speed = 4

        for layer in self.tmx_map:
            for x, y, gid in layer:
                tile = self.tmx_map.get_tile_image_by_gid(gid)
                if tile:
                    if layer.name == "platforms":
                        platform = Platform(tile, x * self.tmx_map.tilewidth,
                                            y * self.tmx_map.tilewidth,
                                            self.tmx_map.tilewidth,
                                            self.tmx_map.tileheight)
                        self.all_sprites.add(platform)
                        self.platforms.add(platform)
                    elif layer.name == "crabs":
                        crab = Crab(self.map_pixel_width,
                                    self.map_pixel_height, x * self.tmx_map.tilewidth * TILE_SCALE,
                                    y * self.tmx_map.tileheight * TILE_SCALE)
                        self.all_sprites.add(crab)
                        self.enemies.add(crab)
                    elif layer.name == "pumpkins":
                        robo_pumpkin = RoboPumpkin(self.map_pixel_width,
                                                   self.map_pixel_height, x * self.tmx_map.tilewidth * TILE_SCALE,
                                                   y * self.tmx_map.tileheight * TILE_SCALE)
                        self.all_sprites.add(robo_pumpkin)
                        self.enemies.add(robo_pumpkin)
                    elif layer.name == "coins":
                        coin = Coin(x * self.tmx_map.tilewidth,
                                    y * self.tmx_map.tilewidth)
                        self.all_sprites.add(coin)
                        self.coins.add(coin)
                    elif layer.name == "portals":
                        portal = Portal(x * self.tmx_map.tilewidth,
                                        y * self.tmx_map.tilewidth)
                        self.all_sprites.add(portal)
                        self.portals.add(portal)

                    else:
                        platform = Platform(tile, x * self.tmx_map.tilewidth,
                                            y * self.tmx_map.tilewidth,
                                            self.tmx_map.tilewidth,
                                            self.tmx_map.tileheight)
                        self.all_sprites.add(platform)

        self.collected_coins = 0
        self.coins_amount = len(self.coins)

        self.run()

    def run(self):
        self.is_running = True
        while self.is_running:
            self.event()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pg.quit()
        quit()

    # def event(self):
    #     for event in pg.event.get():
    #         if event.type == pg.QUIT:
    #             self.is_running = False
    def event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.is_running = False
            if self.mode == "game over":
                if event.type == pg.KEYDOWN:
                    self.setup()
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    shoot.play()
                    if self.player.current_animation in (
                            self.player.idle_animation_right, self.player.running_animation_right):
                        ball = Ball(self.player.rect, "right")
                    elif self.player.current_animation in (
                            self.player.idle_animation_left, self.player.running_animation_left):
                        ball = Ball(self.player.rect, "left")
                        # if ball.rect.y < 0:
                        #     ball.kill()

                    self.all_sprites.add(ball)
                    self.balls.add(ball)

    def update(self):
        self.player.update(self.platforms)
        self.balls.update(self.player.rect.x - SCREEN_WIDTH // 2,
                          self.player.rect.x + SCREEN_WIDTH // 2)
        self.enemies.update(self.platforms)
        self.coins.update()
        self.portals.update()
        if self.player.hp <= 0:
            self.mode = "game over"
            return
        for enemy in self.enemies.sprites():
            if pg.sprite.collide_mask(self.player, enemy):
                self.player.get_damage()

        if self.player.rect.y >= self.map_pixel_height + 300:
            self.player.hp = 0

        pg.sprite.groupcollide(self.balls, self.enemies, True, True)
        pg.sprite.groupcollide(self.balls, self.platforms, True, False)
        hits = pg.sprite.spritecollide(self.player, self.coins, True)

        if pg.sprite.spritecollide(self.player, self.portals, False):
            if self.collected_coins > self.coins_amount // 2:
                self.level += 1
                self.setup()
        for hit in hits:
            self.collected_coins += 1
            coin.play()

        self.camera_x = self.player.rect.x - SCREEN_WIDTH // 2
        self.camera_y = self.player.rect.y - SCREEN_HEIGHT // 2

        self.camera_x = max(0, min(self.camera_x, self.map_pixel_width - SCREEN_WIDTH))  # Построение границ карты
        self.camera_y = max(0, min(self.camera_y, self.map_pixel_height - SCREEN_HEIGHT))

    def draw(self):
        # self.screen.fill("light blue")
        self.screen.blit(self.background, (0, 0))

        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, sprite.rect.move(-self.camera_x, -self.camera_y))

        pg.draw.rect(self.screen, pg.Color("red"), (5, 5, self.player.hp * 20, 20))
        pg.draw.rect(self.screen, pg.Color("black"), (5, 5, 200, 20), 3)
        coin_text = font.render(f"Coins {self.collected_coins}", True, pg.Color("Black"))
        coin_text_rect = coin_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
        self.screen.blit(coin_text, coin_text_rect)
        if self.mode == "game over":
            text = font.render("Game over", True, pg.Color("Red"))
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(text, text_rect)

        pg.display.flip()


if __name__ == "__main__":
    game = Game()
