import os

# Adres IP serwera
HOST = 'localhost'
PORT = 12345

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CARDS = os.path.join(BASE_DIR, 'TextFiles', 'cards.txt')