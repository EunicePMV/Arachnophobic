import pygame, sys, csv

pygame.init()

clock = pygame.time.Clock()
FPS = 60

# GAME WINDOW
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 800

# GAME VARIABLES 
ROWS = 18
MAX_COLS = 96
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 87

# GAME COLOR 
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BROWN = (61, 37, 59)

# SCROLLING EFFECT TO THE RIGHT 
scroll_left = False
scroll_right = False
scroll = 0
scroll_speed = 1 

# SETTING THE WINDOW 
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Arachnophobic')

# LOADING TILES IMAGES 
img_list = []
for x in range(1, TILE_TYPES + 1):
    img = pygame.image.load(f'./img/tile_types/Tile_{x}.png').convert_alpha()
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)

# DRAW BACKGROUND COLOR 
def draw_bg():
    screen.fill(BROWN)

# DRAW THE GRID MAP
# def draw_grid():
#     # vertical lines
#     for c in range(MAX_COLS + 1):
#         pygame.draw.line(screen, RED, (c * TILE_SIZE - scroll, 0), (c * TILE_SIZE - scroll, SCREEN_HEIGHT))

#     # horizontal lines
#     for c in range(ROWS + 1):
#         pygame.draw.line(screen, RED, (0, c * TILE_SIZE), (SCREEN_WIDTH, c * TILE_SIZE))

forest_map = []
for row in range(ROWS):
    r = [-1] * MAX_COLS
    forest_map.append(r)

with open('level1_data.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            forest_map[x][y] = int(tile)     

# DRAW TILES 
def draw_world():
    for y, row in enumerate(forest_map):
        for x, tile in enumerate(row):
            if tile >= 0:
                screen.blit(img_list[tile], (x * TILE_SIZE - scroll, y * TILE_SIZE))

running = True
while running:

    clock.tick(FPS)

    draw_bg()
    # draw_grid()
    draw_world()
    
    # SCROLL THE MAP
    if scroll_left == True and scroll > 0:
        scroll -= 5* scroll_speed
    if scroll_right == True and scroll < (MAX_COLS * TILE_SIZE) - SCREEN_WIDTH:
        scroll += 5 * scroll_speed

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                scroll_left = True
            if event.key == pygame.K_RIGHT:
                scroll_right = True
            if event.key == pygame.K_RSHIFT:
                scroll_speed = 5 
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                scroll_left = False
            if event.key == pygame.K_RIGHT:
                scroll_right = False
            if event.key == pygame.K_RSHIFT:
                scroll_speed = 1

    # screen.fill('black')
    pygame.display.update()

pygame.quit()
