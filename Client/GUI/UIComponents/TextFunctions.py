# Funkcja rysująca tekst zaczynając od lewego górnego punktu, wycentrowany do puntku
def draw_text(surface, text, color, x, y, font, center: bool):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    surface.blit(text_surface, text_rect)

# Zczytanie tekstu z pliku
def read_text_from_file(filename):
    with open(filename, "r") as file:
        text = file.read()
    return text

# Rysowanie tekstu z możliwością scrollowania
def render_text_scrolled(screen, font, text, scroll, color, line_spacing, rect, padding):
    y_offset = padding
    for line in text.split("\n"):
        for small_line in split_line_by_width(line, font, rect.width - 10 * padding):
            rendered_line = font.render(small_line, True, color)
            text_rect = rendered_line.get_rect(topleft=(rect.left + padding, rect.top + y_offset - scroll))
            if rect.contains(text_rect):
                screen.blit(rendered_line, text_rect.topleft)
            y_offset += rendered_line.get_height() + line_spacing

# Dzieli zbyt długi tekst na krótsze linijki
def split_line_by_width(line, font, width):
    total_width = 0
    start_index = 0
    end_index = 0
    splitted = []
    
    while end_index < len(line):
        letter_width, _ = font.size(line[end_index])
        if total_width + letter_width >= width:
            curr_line: str = line[start_index:end_index]
            last_space = curr_line.rfind(' ') 
            if last_space != -1:
                end_index = start_index + last_space + 1
            splitted.append(line[start_index:end_index])
            start_index = end_index
            total_width = 0
        else:
            total_width += letter_width
            end_index += 1
    splitted.append(line[start_index:])

    return splitted