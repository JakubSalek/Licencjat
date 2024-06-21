import os

# Server IP
HOST = "127.0.0.1"
PORT = 12345

# Kolory
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (128, 128, 128)
BETTER_GRAY = (204, 202, 202)
YELLOW = (255, 255, 0)

# Kolory dla komponentów
BG_COLOR = (0, 0, 0)
BUTTON_COLOR = (51, 204, 51)
BUTTON_HOVER_COLOR = (0, 153, 51)
FONT_COLOR = (255, 255, 255)
FONT_COLOR2 = (0, 0, 0)
TILE_COLOR = (204, 153, 0)
TILE_BORDER_COLOR = (102, 51, 0)
PLAYER_COLORS = [(255, 0, 0), (0, 255, 0), (153, 204, 255), (255, 0, 255)]

# Ustawienia pygame
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 360
WINDOW_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
FPS = 60

# Dostępne ustawienia
RESOLUTION = [(640, 360), (800, 600),(1280, 720), (1280, 800), (1280, 1024), (1366, 768), (1440, 900), (1600, 900), (1920, 1080), (1920, 1200)]
CAN_FPS = [30, 60, 90, 120]
FULLSCREEN = False

# Pliki pomocnicze
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HOW_TO_FILE = os.path.join(BASE_DIR, 'TextFiles', 'how_to_play.txt')
FONT = os.path.join(BASE_DIR, 'Fonts', 'arial.ttf')
CARDS = os.path.join(BASE_DIR, 'TextFiles', 'cards.txt')

# Ustawienia gry
TILE_COUNT = 100
TILES_ROW = 10
TILES_COL = 5

# DEBUG
DEBUG = True
