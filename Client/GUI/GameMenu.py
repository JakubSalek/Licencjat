import math
from GUI.Menu import Menu
from GUI.UIComponents import draw_text, Button
import pygame as pg
import SETTINGS as S


class TileItem:
    def __init__(self, width, height) -> None:
        self.swidth = width
        self.sheight = height
        self.surface = pg.Surface((width, height), pg.SRCALPHA)
        self.rect = self.surface.get_rect()
        self.player_width = self.swidth // 2
        self.player_height = self.sheight // 2
        self.player_radius = self.swidth // 6
    
    def draw(self, players):
        self.surface.fill(S.TILE_COLOR)
        for i, player in enumerate(players):
            posx = (i % 2) * self.player_width + self.player_radius + (self.swidth // 10)
            posy = (i // 2) * self.player_height + self.player_radius + (self.sheight // 14)
            pg.draw.circle(self.surface, player.color, (posx, posy), self.player_radius)


class PlayerItem:
    def __init__(self, player, font, width, height):
        self.swidth = width
        self.sheight = height
        self.surface = pg.Surface((width, height))
        self.player = player
        self.font = font
        self.rect = self.surface.get_rect()

    def draw(self):
        self.surface.fill(self.player.color)
        draw_text(self.surface, self.player.nickname, S.BLACK, self.swidth//2, self.sheight * 0.2, self.font, True)
        draw_text(self.surface, f"Gold: {self.player.gold}", S.BLACK, self.swidth//2, self.sheight * 0.45, self.font, True)
        draw_text(self.surface, f"Progress: {self.player.progress+1}/{S.TILE_COUNT}", S.BLACK, self.swidth//2, self.sheight * 0.75, self.font, True)


class GameMenu(Menu):
    def __init__(self, gui, table, is_owner):
        super().__init__(gui)   
        self.table = table
        self.owner = is_owner
        self.table_alive = True
        self.show_move = True
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

        # Move Rect
        self.my_move = is_owner
        self.mrect_width = self.trect_width * 0.8
        self.mrect_height = self.trect_height * 0.8
        self.card_rect = pg.Rect(S.SCREEN_WIDTH * 0.1, S.SCREEN_HEIGHT * 0.1,
                                self.mrect_width//2, self.mrect_height)
        self.choice_rect = pg.Rect(S.SCREEN_WIDTH * 0.1 + self.mrect_width//2, S.SCREEN_HEIGHT * 0.1,
                                self.mrect_width//2, self.mrect_height)

        # Przyciski
        self.move_button = Button((S.TILES_ROW - 1) * self.tile_width + self.tile_width * 0.1,
                                    (S.TILES_COL - 1) * self.tile_height + self.tile_height * 0.4,
                                    self.tile_width * 0.8, self.tile_height * 0.5, "Move", self.gui.xs_font,
                                    S.BUTTON_COLOR, S.BUTTON_HOVER_COLOR)
        self.buttons.append(self.move_button)

        # Scroll planszy
        self.board_scroll = 0
        self.board_button_scroll_speed = self.tile_height
        self.board_mouse_scroll_speed = self.tile_height
        total_rows = math.ceil(S.TILE_COUNT / S.TILES_ROW)
        total_height = total_rows * self.tile_height
        self.board_scrollable_height = max(0, total_height - self.trect_height)
        
        # Scroll tekstu na karcie
        self.card_scroll = 0
        self.card_text_padding = 10
        self.card_line_spacing = 5
        self.card_button_scroll_speed = 5
        self.card_mouse_scroll_speed = self.card_button_scroll_speed * 10


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
                        # if self.delete_button.rect.collidepoint(event.pos):
                        if self.move_button.rect.collidepoint(event.pos):
                            self.show_move = not self.show_move
                    elif event.button == 4:
                        if self.show_move:
                            self.card_scroll -= self.card_mouse_scroll_speed if self.card_scroll > 0 else 0
                        else:
                            self.board_scroll -= self.board_mouse_scroll_speed if self.board_scroll > 0 else 0
                    elif event.button == 5:
                        if self.show_move:
                            self.card_scroll += self.card_mouse_scroll_speed
                        else:
                            self.board_scroll += self.board_mouse_scroll_speed if self.board_scroll < self.board_scrollable_height else 0
            keys = pg.key.get_pressed()
            if keys[pg.K_UP]:
                if self.show_move:
                    self.card_scroll -= self.card_button_scroll_speed if self.card_scroll > 0 else 0
                else:
                    self.board_scroll -= self.board_button_scroll_speed if self.board_scroll > 0 else 0
            elif keys[pg.K_DOWN]:
                if self.show_move:
                    self.card_scroll += self.card_button_scroll_speed
                else:
                    self.board_scroll += self.board_button_scroll_speed if self.board_scroll < self.board_scrollable_height else 0

            self.draw()
            self.check_server()

    def draw_move(self, screen):
        # Rysowanie karty
        pg.draw.rect(screen, S.BLACK, self.card_rect)
        pg.draw.rect(screen, S.WHITE, self.card_rect, 2)

        # Rysowanie możliwości
        pg.draw.rect(screen, S.BLACK, self.choice_rect)
        pg.draw.rect(screen, S.WHITE, self.choice_rect, 2)


    def draw(self):
        screen = self.gui.screen
        clock = self.gui.clock
        
        # Rysowanie menu
        screen.fill(S.BG_COLOR)

        # Wyrysowanie tile na górze
        for i in range(S.TILE_COUNT):
            tile_rect = pg.Rect(self.tiles_rect.left + (i % S.TILES_ROW) * self.tile_width,
                                self.tiles_rect.top + (i // S.TILES_ROW) * self.tile_height - self.board_scroll,
                                self.tile_width, self.tile_height)
            if self.tiles_rect.contains(tile_rect):
                tile_sprite = TileItem(self.tile_width, self.tile_height)
                tile_sprite.rect.topleft = (self.tiles_rect.left + (i % S.TILES_ROW) * self.tile_width,
                                            self.tiles_rect.top + (i // S.TILES_ROW) * self.tile_height - self.board_scroll)
                players = []
                for player in self.table.players:
                    if player.progress == i:
                        players.append(player)
                tile_sprite.draw(players)
                screen.blit(tile_sprite.surface, tile_sprite.rect.topleft)
                pg.draw.rect(screen, S.TILE_BORDER_COLOR, tile_sprite.rect, 2)
        

        # Wyrysowanie graczy na dole ekranu
        pg.draw.rect(screen, S.WHITE, self.players_rect, 2)
        for i, player in enumerate(self.table.players):
            player_rect = pg.Rect(self.players_rect.left + i * self.player_width, self.players_rect.top,
                                self.player_width, self.prect_height)
            player_sprite = PlayerItem(player, self.gui.xs_font, self.player_width, self.prect_height)
            player_sprite.rect = player_rect
            player_sprite.draw()
            screen.blit(player_sprite.surface, player_sprite.rect)
            pg.draw.rect(screen, S.WHITE, player_sprite.rect, 2)

        if self.show_move:
            self.draw_move(screen)

        # Rysowanie przycisków
        for button in self.buttons:
            button.draw(screen)

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