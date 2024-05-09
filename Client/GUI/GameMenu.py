from GUI.Menu import Menu
from GUI.UIComponents import draw_text
from Player import Player
import pygame as pg
import SETTINGS as S


class TileItem:
    def __init__(self, width, height) -> None:
        self.swidth = width
        self.sheight = height
        self.surface = pg.Surface((width, height))
        self.rect = self.surface.get_rect()
        self.player_width = self.swidth // 2
        self.player_height = self.sheight // 2
        self.player_radius = self.swidth // 4
    
    def draw(self, screen, player_count):
        self.surface.fill(S.TILE_COLOR)
        pg.draw.rect(screen, S.TILE_BORDER_COLOR, self.rect, 2)
        for i in range(player_count):
            posx = (i%2) * self.player_width + self.player_radius
            posy = (i//2) * self.player_height + self.player_radius
            pg.draw.circle(self.surface, S.PLAYER_COLORS[i], (posx, posy), self.player_radius)


class PlayerItem:
    def __init__(self, player, font, width, height):
        self.swidth = width
        self.sheight = height
        self.surface = pg.Surface((width, height))
        self.player = player
        self.font = font
        self.rect = self.surface.get_rect()

    def draw(self, screen):
        self.surface.fill(S.BETTER_GRAY)
        pg.draw.rect(screen, S.BLACK, self.rect, 2)
        draw_text(self.surface, self.player.nickname, S.BLACK, self.swidth//2, self.sheight * 0.2, self.font, True)
        draw_text(self.surface, f"Gold: {self.player.gold}", S.BLACK, self.swidth//2, self.sheight * 0.45, self.font, True)
        draw_text(self.surface, f"Progress: {self.player.progress+1}/{S.TILE_COUNT}", S.BLACK, self.swidth//2, self.sheight * 0.75, self.font, True)

class GameMenu(Menu):
    def __init__(self, gui, table, is_owner):
        super().__init__(gui)   
        self.table = table
        self.owner = is_owner
        self.table_alive = True
        self.buttons = []

        # Players Rect
        self.prect_width = S.SCREEN_WIDTH
        self.prect_height = S.SCREEN_HEIGHT*0.3
        self.players_rect = pg.Rect(0, S.SCREEN_HEIGHT*0.7,
                                    self.prect_width, self.prect_height)
        self.player_width = self.prect_width//4
        
        # Tiles Rect
        self.trect_width = S.SCREEN_WIDTH
        self.trect_height = S.SCREEN_HEIGHT - self.prect_height
        self.tiles_rect = pg.Rect(0, 0, self.trect_width, self.trect_height)
        self.tile_width = self.trect_width // S.TILES_ROW
        self.tile_height = self.trect_height // S.TILES_COL
        self.scroll = 0
        self.button_scroll_speed = 3
        self.mouse_scroll_speed = self.button_scroll_speed * 5
        self.scrollable_height =  (S.TILES_ROW + 1) * (2 * self.tile_height) - self.trect_height

        self.run()
        
    def run(self):
        # Główna pętla menu
        while self.table_alive:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    if self.owner:
                        self.gui.client.delete_table(self.table)
                    else:
                        self.gui.client.leave_table(self.table)
                    self.close_program()
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        # TODO obsługa guzików przy kartach
                        pass
                        # if self.delete_button.rect.collidepoint(event.pos):
                    elif event.button == 4:
                        self.scroll -= self.mouse_scroll_speed if self.scroll > 0 else 0
                        self.refresh_tables = True
                    elif event.button == 5:
                        self.scroll += self.mouse_scroll_speed if self.scroll < self.scrollable_height else 0
                        self.refresh_tables = True
            keys = pg.key.get_pressed()
            if keys[pg.K_UP]:
                self.scroll -= self.button_scroll_speed if self.scroll > 0 else 0
                self.refresh_tables = True
            elif keys[pg.K_DOWN]:
                self.scroll += self.button_scroll_speed if self.scroll < self.scrollable_height else 0
                self.refresh_tables = True

            self.draw()
            self.check_server()

    def draw(self):
        screen = self.gui.screen
        clock = self.gui.clock
        
        # Rysowanie menu
        screen.fill(S.BG_COLOR)
        
        # Rysowanie przycisków
        for button in self.buttons:
            button.draw(screen)

        # Wyrysowanie tile na górze
        for i in range(S.TILE_COUNT):
            tile_rect = pg.Rect(self.tiles_rect.left + (i % S.TILES_ROW) * self.tile_width,
                                self.players_rect.top + (i // S.TILES_ROW) * self.tile_height - self.scroll,
                                self.tile_width, self.tile_height)
            if self.tiles_rect.contains(tile_rect):
                tile_sprite = TileItem(self.gui.xs_font, self.tile_width, self.tile_height)
                tile_sprite.rect = tile_rect
                player_count = 0
                for player in self.table.players:
                    if player.progress == i:
                        player_count += 1
                tile_sprite.draw(screen, player_count)
                screen.blit(tile_sprite.surface, tile_sprite.rect)
        

        # Wyrysowanie graczy na dole ekranu
        pg.draw.rect(screen, S.WHITE, self.players_rect, 2)
        for i, player in enumerate(self.table.players):
            player_rect = pg.Rect(self.players_rect.left + i * self.player_width, self.players_rect.top,
                                self.player_width, self.prect_height)
            player_sprite = PlayerItem(player, self.gui.xs_font, self.player_width, self.prect_height)
            player_sprite.rect = player_rect
            pg.draw.rect(screen, S.WHITE, player_sprite.rect, 2)
            player_sprite.draw(screen)
            screen.blit(player_sprite.surface, player_sprite.rect)

        # Odświeżenie ekranu
        pg.display.flip()
        clock.tick(S.FPS)

        # Sprawdzenie najechania myszką
        mouse_pos = pg.mouse.get_pos()
        for button in self.buttons:
            if button.active:
                button.check_hover(mouse_pos)

    def check_server(self):
        while not self.gui.message_queue.empty():
            message: str = self.gui.message_queue.get_nowait()
            if message.startswith("PlayersList"):
                splitted = message.split(";")
                splitted = splitted[1:]
                for player in self.table.players:
                    player.found = False

                for i in range(len(splitted)//2):
                    id = splitted[i * 2]
                    for player in self.table.players:
                        if id == player.id:
                            player.found = True

                for player in self.table.players:
                    if not player.found:
                        self.table.players.remove(player)
            elif message == "DeletedTable":
                self.table_alive = False
            else:
                print(f"Unhandled message \"{message}\"") if S.DEBUG else None

            
    def close_program(self):
        return super().close_program()