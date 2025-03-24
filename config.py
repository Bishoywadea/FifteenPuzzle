import pygame as pg

# Declare some constants and variables
FPS = 45
WHITE = pg.Color("#DDDDDD")
BLACK = pg.Color("#1A1A1A")
GREY = pg.Color("#333333")
ORANGE = pg.Color("#FF6600")
RED = pg.Color("#FF1F00")

# 15 Puzzle specific settings
BOARD_SIZE = 480
TILE_SIZE = BOARD_SIZE // 4
LINE_WIDTH = 6
CIRCLE_RADIUS = 8
CIRCLE_WIDTH = 2
FRAME_GAP = 80  
GRID_ROWS = 4        
GRID_COLS = 4 

def init():
    global WIN, WIDTH, HEIGHT
    WIN = pg.display.get_surface()
    WIDTH, HEIGHT = WIN.get_size()