import pygame
import sys
import SETTINGS as S

# Funkcja rysująca tekst na ekranie
def draw_text(surface, text, color, x, y):
    text_surface = S.FONT.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_surface, text_rect)

# Funkcja główna menu
def settings_menu(screen):
    clock = pygame.time.Clock()
    input_box = pygame.Rect(100, S.SCREEN_HEIGHT / 2 - 20, S.SCREEN_WIDTH - 200, 40)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        print(text)
                        # Tutaj można umieścić kod, który ma zostać wykonany po wpisaniu tekstu
                        text = ''
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.fill(S.WHITE)
        pygame.draw.rect(screen, color, input_box, 2)
        draw_text(screen, 'Enter your name:', S.TEXT_COLOR, 100, S.SCREEN_HEIGHT / 2 - 50)
        draw_text(screen, text, S.TEXT_COLOR, input_box.x + 5, input_box.y + 5)
        pygame.display.flip()
        clock.tick(S.FPS)