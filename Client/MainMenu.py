import pygame
import sys
from SettingsMenu import settings_menu

# Inicjalizacja Pygame
pygame.init()

# Ustawienia ekranu
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Menu Główne")

# Kolory
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Klasy przycisków
class Button:
    def __init__(self, x, y, width, height, text, font, normal_color, hover_color, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.normal_color = normal_color
        self.hover_color = hover_color
        self.action = action
        self.hovered = False

    def draw(self, surface):
        color = self.hover_color if self.hovered else self.normal_color
        pygame.draw.rect(surface, color, self.rect)
        text_surface = self.font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def check_hover(self, pos):
        self.hovered = self.rect.collidepoint(pos)

# Funkcja wyświetlająca menu główne
def main_menu():
    font = pygame.font.Font(None, 36)

    # Przyciski menu
    play_button = Button(300, 200, 200, 50, "Gra sieciowa", font, GRAY, WHITE)
    settings_button = Button(300, 270, 200, 50, "Ustawienia", font, GRAY, WHITE)
    quit_button = Button(300, 340, 200, 50, "Zakończ", font, GRAY, WHITE)

    # Główna pętla menu
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if play_button.rect.collidepoint(event.pos):
                        # Akcja po naciśnięciu przycisku "Gra sieciowa"
                        print("Przejście do gry sieciowej")
                    elif settings_button.rect.collidepoint(event.pos):
                        # Akcja po naciśnięciu przycisku "Ustawienia"
                        settings_menu()
                    elif quit_button.rect.collidepoint(event.pos):
                        # Akcja po naciśnięciu przycisku "Zakończ"
                        pygame.quit()
                        sys.exit()

        # Rysowanie menu
        screen.fill(BLACK)
        play_button.draw(screen)
        settings_button.draw(screen)
        quit_button.draw(screen)
        pygame.display.flip()

        # Sprawdzenie najechania myszką
        mouse_pos = pygame.mouse.get_pos()
        play_button.check_hover(mouse_pos)
        settings_button.check_hover(mouse_pos)
        quit_button.check_hover(mouse_pos)

# Uruchomienie menu głównego
if __name__ == "__main__":
    main_menu()
