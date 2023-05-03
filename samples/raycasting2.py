import pygame as pg, numpy as np, math
from pygame.math import Vector2 as vec2



RED = (225, 20, 20)
BLUE = (20, 20, 225)
YELLOW = (225, 225, 20)
BLACK = (20, 20, 20)
WHITE = (250, 250, 250)

COLOR_KEY = (77, 77, 77)

SIZE = vec2((640, 320))

U_KEY = pg.K_w
L_KEY = pg.K_a
R_KEY = pg.K_d 
D_KEY = pg.K_s

screen_display = pg.display.set_mode(SIZE)
time = pg.time.Clock()
playing = True

simple_map = [
    "aaaaaaaaaa",
    "abbbbbbbba",
    "abbbaabbba",
    "abbbbbbbba",
    "aaaaaaaaaa"
]
tile_size = 64
class Ray(pg.sprite.Sprite):
    def __init__(self, surf: pg.Surface):
        pg.sprite.Sprite.__init__(self)
        self.image = surf
        self.rect = surf.get_rect()

class Player(pg.sprite.Sprite):
    def __init__(self, surf: pg.Surface):
        pg.sprite.Sprite.__init__(self)
        self.image = surf
        self.rect = surf.get_rect()
        self.speed = 1
        self.angle = 0
        self.direct = vec2(0, 0)

    def drawSelf(self):
        # self.image.fill((220, 220, 220))
        # pg.draw.rect(self.image, BLUE, (0, 0, self.rect.width, self.rect.height))
        pg.draw.polygon(self.image, BLUE, [(self.rect.width, self.rect.height), (0, self.rect.height), (self.rect.width/2, 0)])

    def moveSelf(self):
        self.rect.x += self.direct.x * self.speed
        self.rect.y += self.direct.y * self.speed

    def rPlayer(self) -> pg.Surface:
        rotated_image = pg.transform.rotate(self.image, self.angle)
        rotated_image.set_colorkey((200, 200, 200))
        return rotated_image

class Tile(pg.sprite.Sprite):
    def __init__(self, tile: pg.Surface):
        pg.sprite.Sprite.__init__(self)
        self.image = tile
        self.rect = tile.get_rect()
    
openTile = pg.Surface((tile_size, tile_size))
openTile.fill(WHITE)

closeTile = pg.Surface((tile_size, tile_size))
closeTile.fill(RED)

player = pg.Surface((tile_size//2, tile_size//2), pg.SRCALPHA)
player.fill((200, 200, 200))
player.set_colorkey((200, 200, 200))
player = Player(player)
player.rect.x = SIZE.x//2
player.rect.y = SIZE.y//2
openTiles = pg.sprite.Group()
closeTiles = pg.sprite.Group()

for row in range(len(simple_map)):
    for col in range(len(simple_map[row])):
        if simple_map[row][col] == "a":
            tile = Tile(closeTile)
            tile.rect.x, tile.rect.y = vec2((col*tile_size, row*tile_size))
            closeTiles.add(tile)
        if simple_map[row][col] == "b":
            tile = Tile(openTile)
            tile.rect.x, tile.rect.y  = vec2((col*tile_size, row*tile_size))
            openTiles.add(tile)

ray = pg.Surface((8, 8))
ray.fill((255, 255, 255))
ray.set_colorkey((255, 255, 255))
pg.draw.circle(ray, YELLOW, (2, 2), 4)
ray = Ray(ray)
rays = pg.sprite.Group()
for i in range(8): rays.add(ray)

def raycast(surf: pg.Surface, angle: float, initial_pos: vec2, depth: float):
    pts = []
    fov = math.pi / 4
    half_fov = fov / 2
    casted_rays = 8
    initial_angle = angle - half_fov
    
    ray: Ray
    for ray in rays.sprites():
        coords = vec2(
            initial_pos.x + math.sin(initial_angle) * depth,
            initial_pos.y - math.cos(initial_angle) * depth
        )
        ray.rect.x, ray.rect.y = coords.x, coords.y
        initial_angle += fov/casted_rays
    rays.draw(screen_display)
    return rays

pg.init()
t = 0
while playing:
    t+=1
    openTiles.draw(screen_display)
    closeTiles.draw(screen_display)

    player.drawSelf()
    player.angle = -math.degrees(math.atan2(pg.mouse.get_pos()[1] - player.rect.y, pg.mouse.get_pos()[0] - player.rect.x)+ math.pi/2)
    rotatedP = player.rPlayer()
    screen_display.blit(rotatedP, (player.rect.x - int(rotatedP.get_width() / 2), player.rect.y - int(rotatedP.get_height()/2)))
    raycast(screen_display, math.radians(-player.angle), vec2(player.rect.x, player.rect.y), t*0.1)
    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            playing = False
        if event.type == pg.KEYDOWN:
            if event.key == U_KEY:
                player.direct.y = -1
            if event.key == D_KEY:
                player.direct.y = 1
            if event.key == R_KEY:
                player.direct.x = 1
            if event.key == L_KEY:
                player.direct.x = -1
            print(player.rect)
        if event.type == pg.KEYUP:
            if event.key == U_KEY:
                player.direct.y = 0
            if event.key == D_KEY:
                player.direct.y = 0
            if event.key == R_KEY:
                player.direct.x = 0
            if event.key == L_KEY:
                player.direct.x = 0

    player.moveSelf()

    pg.display.flip()
    time.tick(120)


