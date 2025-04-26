import pygame as pg


class Ball(pg.sprite.Sprite):
    def __init__(self, player_rect, direction):
        super(Ball, self).__init__()

        self.direction = direction
        self.speed = 10

        self.image = pg.image.load("Sprite pack 4/1 - Agent_Mike_Bullet (16 x 16).png")
        self.image = pg.transform.scale(self.image, (30, 30))

        self.rect = self.image.get_rect()

        if self.direction == "right":
            self.rect.x = player_rect.right - 13
        elif self.direction == "left":
            self.image = pg.transform.flip(self.image,True,False)
            self.rect.right = player_rect.left +13


        self.rect.centery = player_rect.centery + 20

    def update(self,left_edge,right_edge):
        if self.direction == "right":
            self.rect.x += self.speed
        elif self.direction == "left":
            self.rect.x -= self.speed

        if self.rect.right < left_edge or self.rect.left > right_edge:
            self.kill()





