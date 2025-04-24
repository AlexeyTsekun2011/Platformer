import pygame as pg
import pytmx
from constants import *
from Crab import Crab
from robo_pumpkin import RoboPumpkin
from ball import Ball
from player import Player
# pip install pytmx
pg.init()

font = pg.font.Font(None, 72)


class Platform(pg.sprite.Sprite):
    def __init__(self, image, x, y, width, height):
        super().__init__()
        self.image = pg.transform.scale_by(image, TILE_SCALE)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SCALE
        self.rect.y = y * TILE_SCALE



class Game:
    def __init__(self):
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption("Платформер")
        self.clock = pg.time.Clock()
        self.is_running = False

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

        self.tmx_map = pytmx.load_pygame("level1.tmx")
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

                    else:
                        platform = Platform(tile, x * self.tmx_map.tilewidth,
                                            y * self.tmx_map.tilewidth,
                                            self.tmx_map.tilewidth,
                                            self.tmx_map.tileheight)
                        self.all_sprites.add(platform)

        self.run()

    def run(self):
        self.is_running = True
        while self.is_running:
            self.event()
            self.start_over()
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
        if self.player.hp <= 0:
            self.mode = "game over"
            return
        for enemy in self.enemies.sprites():
            if pg.sprite.collide_mask(self.player, enemy):
                self.player.get_damage()

        pg.sprite.groupcollide(self.balls,self.enemies,True,True)
        pg.sprite.groupcollide(self.balls,self.platforms,True,False)


        self.camera_x = self.player.rect.x - SCREEN_WIDTH // 2
        self.camera_y = self.player.rect.y - SCREEN_HEIGHT // 2
        self.player.update(self.platforms)
        self.balls.update()
        self.camera_x = max(0, min(self.camera_x, self.map_pixel_width - SCREEN_WIDTH))  # Построение границ карты
        self.camera_y = max(0, min(self.camera_y, self.map_pixel_height - SCREEN_HEIGHT))


    def start_over(self):
        if self.player.rect.y > self.map_pixel_height:
            game = Game()



    def draw(self):
        # self.screen.fill("light blue")
        self.screen.blit(self.background, (0, 0))

        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, sprite.rect.move(-self.camera_x, -self.camera_y))

        pg.draw.rect(self.screen, pg.Color("red"), (5, 5, self.player.hp * 20, 20))
        pg.draw.rect(self.screen, pg.Color("black"), (5, 5, 200, 20), 3)
        if self.mode == "game over":
            text = font.render("Игра окончена", True, pg.Color("Red"))
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(text, text_rect)

        pg.display.flip()


if __name__ == "__main__":
    game = Game()
