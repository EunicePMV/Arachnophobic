
# RAYCASTING VIDEO
# https://www.youtube.com/watch?v=AjPPhx8-lXg&t=2162s

# DIMENSION: 64-96 * 16

import pygame
import button
import csv 

pygame.init()

# to set the scroll time of the background
clock = pygame.time.Clock()
FPS = 60

# game window 
SCREEN_WIDTH = 600 #  900
SCREEN_HEIGHT = 450 #  800
LOWER_MARGIN = 350
SIDE_MARGIN = 900

# set the screen size 
screen = pygame.display.set_mode((SCREEN_WIDTH + SIDE_MARGIN, SCREEN_HEIGHT + LOWER_MARGIN))
# screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Arachnophobic')

# define game variables
# divide rows to the screen_height to have appropriate screen tiles 
ROWS = 18
MAX_COLS = 96
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 87
level = 0
current_tile = 0

# ROWS = 16
# MAX_COLS = 150
# TILE_SIZE = SCREEN_HEIGHT // ROWS 


scroll_left = False
scroll_right = False 
scroll = 0
scroll_speed = 1 

# load images
# pine1_img = pygame.image.load('img/Background/pine1.png').convert_alpha()
# pine2_img = pygame.image.load('img/Background/pine2.png').convert_alpha()
# mountain_img = pygame.image.load('img/Background/mountain.png').convert_alpha()
# sky_img = pygame.image.load('img/Background/sky.png').convert_alpha()
# background_img = pygame.image.load('./img/Background/Background.png').convert_alpha()
# store tiles in list 
img_list = []
# load all of the tiles
for x in range(1, TILE_TYPES + 1):
    img = pygame.image.load(f'./img/tile_types/Tile_{x}.png').convert_alpha()
    # set tiles loaded to the size of TILE_SIZE
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)

save_img = pygame.image.load('./img/save_btn.png').convert_alpha()
load_img = pygame.image.load('./img/load_btn.png').convert_alpha()

# define colors 
# GREEN = (144, 201, 120)
# WHITE = (255, 255, 255)
# RED = (200, 25, 25)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BROWN = (61, 37, 59)

# define font 
font = pygame.font.SysFont('Futura', 30)

# create empty tile list 
world_data = []
# generate the the proxy csv file in a list 
for row in range(ROWS):
    r = [-1] * MAX_COLS
    world_data.append(r)

# set the upper left of the grid with this tile 
world_data[0][0] = 0

# set the bottom left of the grid with this tile
world_data[ROWS - 1][0] = 20

# make this cells set to 0, which means that is the border
for tile in range(1, MAX_COLS):
    # bottom set in grid
    world_data[ROWS - 1][tile] = 21
    # top set in grid
    world_data[0][tile] = 1

# set border in the leftmost indicating this is the leftmost border of the game
for tile in range(1, ROWS - 1):
    world_data[tile][0] = 16

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


# function to draw the background 
def draw_bg():
    # to fill the bakground color of the window
    screen.fill(BROWN)

    # get the width of this background
    # width = background_img.get_width()

    # loop to keep on filling the background of the window with this picture
    # for x in range(4): 
    #     screen.blit(background_img, ((x * width) - scroll * 0.8, 0))

    # screen.fill(GREEN)
    # width = sky_img.get_width()
    # for x in range(4):
    #     screen.blit(sky_img, (-scroll, 0))
    #     screen.blit(mountain_img, ((x * width)-scroll, SCREEN_HEIGHT - mountain_img.get_height() - 300))
    #     screen.blit(pine1_img, (-scroll, SCREEN_HEIGHT - pine1_img.get_height() - 150))
    #     screen.blit(pine2_img, (-scroll, SCREEN_HEIGHT - pine2_img.get_height()))

def draw_grid():
    # vertical lines 
    for c in range(MAX_COLS + 1):
        pygame.draw.line(screen, BLACK, (c * TILE_SIZE - scroll, 0), (c * TILE_SIZE - scroll, SCREEN_HEIGHT))

    for c in range(ROWS + 1):
        pygame.draw.line(screen, BLACK, (0, c * TILE_SIZE), (SCREEN_WIDTH, c * TILE_SIZE))

# function for drawing the world tiles
def draw_world():
    for y, row in enumerate(world_data):
        for x, tile in enumerate(row):
            if tile >= 0:
                screen.blit(img_list[tile], (x * TILE_SIZE - scroll, y *TILE_SIZE))

# create buttons
save_button = button.Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT + LOWER_MARGIN - 50, save_img, 1)
load_button = button.Button(SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT + LOWER_MARGIN - 50, load_img, 1)
# make button list
button_list = []
button_col = 0
button_row = 0
for i in range(len(img_list)):
    # adjust the button here
    tile_button = button.Button(SCREEN_WIDTH + (50 * button_col) + 50, 50 * button_row + 50, img_list[i], 1)
    button_list.append(tile_button)
    button_col += 1

    if button_col == 9:
        button_row += 1
        button_col = 0


# display the screen until there some kind of movement to close the window 
run = True
while run:
    
    clock.tick(FPS)

    draw_bg()
    draw_grid()
    draw_world()

    draw_text(f'Level: {level}', font, BLACK, 10, SCREEN_HEIGHT + LOWER_MARGIN - 120)
    draw_text(f'Press UP or DOWN to change level', font, BLACK, 10, SCREEN_HEIGHT + LOWER_MARGIN - 90)

    # save and load data
    if save_button.draw(screen):
        # save level data
        with open(f'level{level}_data.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            for row in world_data:
                writer.writerow(row)

    if load_button.draw(screen):
        # load in level data
        # reset scroll back to the start of the level
        scroll = 0 
        with open(f'level{level}_data.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for x, row in enumerate(reader):
                for y, tile in enumerate(row):
                    world_data[x][y] = int(tile)

    # draw tile panel and tiles
    pygame.draw.rect(screen, WHITE, (SCREEN_WIDTH, 0, SIDE_MARGIN, SCREEN_HEIGHT))

    # choose a tile
    button_count = 0
    for button_count, i in enumerate(button_list):
        if i.draw(screen):
            current_tile = button_count
    
    # highlight the selected tile
    pygame.draw.rect(screen, BLUE, button_list[current_tile].rect, 3)

    # scroll the map
    # scroll > 0 tells that do not scroll left further than the starting point
    if scroll_left == True and scroll > 0:
        scroll -= 5 * scroll_speed
    if scroll_right == True and scroll < (MAX_COLS * TILE_SIZE) - SCREEN_WIDTH:
        scroll += 5 * scroll_speed

    # add new tiles on the screen
    # get mouse position
    pos = pygame.mouse.get_pos()
    x = (pos[0] + scroll) // TILE_SIZE
    y = pos[1] // TILE_SIZE

    # check that the coordinates are within the tile area
    if pos[0] < SCREEN_WIDTH and pos[1] < SCREEN_HEIGHT:
        # update tile value
        if pygame.mouse.get_pressed()[0] == 1:
            if world_data[y][x] != current_tile:
                world_data[y][x] = current_tile
        if pygame.mouse.get_pressed()[2] == 1:
            world_data[y][x] = -1
    

    # check is there is any event happening while the screen is display
    # if player click close in the window, then quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        # when keys are press
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                scroll_left = True
            if event.key == pygame.K_RIGHT:
                scroll_right = True
            if event.key == pygame.K_RSHIFT:
                scroll_speed = 5 
        
        # when keys are release
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                level += 1
            if event.key == pygame.K_DOWN and level > 0:
                level -= 1
            if event.key == pygame.K_LEFT:
                scroll_left = False
            if event.key == pygame.K_RIGHT:
                scroll_right = False
            if event.key == pygame.K_RSHIFT:
                scroll_speed = 1
        
    pygame.display.update()

pygame.quit()

# how to load the created csv file to a grid map of a map