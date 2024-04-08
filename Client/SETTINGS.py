import pygame

# Server IP
HOST = "127.0.0.1"
PORT = 12345

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
BETTER_GRAY = (204, 202, 202)
YELLOW = (255, 255, 0)

# Pygame settings and constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 800
WINDOW_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
FPS = 60

# Possible settings
RESOLUTION = [(640, 360), (800, 600),(1280, 720), (1280, 800), (1280, 1024), (1366, 768), (1440, 900), (1600, 900), (1920, 1080), (1920, 1200)]
CAN_FPS = [30, 60, 90, 120]
FULLSCREEN = False

# Pliki pomocnicze
HOW_TO_FILE = "Client\\TextFiles\\how_to_play.txt"

FONT = "Client\\TextFiles\\Fonts\\arial.ttf"