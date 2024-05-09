from GUI.UIComponents import draw_text, Button
from GUI.Menu import Menu
from GUI.GameMenu import GameMenu
import pygame as pg
import SETTINGS as S
from Player import Player

class PlayerItem():
    def __init__(self, player, font, width, height):
        self.swidth = width
        self.sheight = height
        self.surface = pg.Surface((width, height))
        self.surface.fill(S.BETTER_GRAY)
        self.player = player
        self.font = font
        self.rect = self.surface.get_rect()

    def draw(self):
        self.surface.fill(S.BETTER_GRAY)
        draw_text(self.surface, "ID: " + str(self.player.id), S.FONT_COLOR2, self.swidth*0.10, self.sheight*0.5, self.font, True)
        draw_text(self.surface, "Name: " + str(self.player.nickname), S.FONT_COLOR2, self.swidth*0.5, self.sheight*0.5, self.font, True)

class TableMenu(Menu):
    def __init__(self, gui, table, is_owner):
        super().__init__(gui)   
        self.table = table
        self.owner = is_owner
        self.table_alive = True
        self.buttons = []
        self.refresh_players = True
        self.player_sprites = []

        self.buttons_width = S.SCREEN_WIDTH * 4/12
        self.buttons_height = S.SCREEN_HEIGHT/12

        if self.owner:
            self.delete_button = Button(S.SCREEN_WIDTH*1/12, S.SCREEN_HEIGHT*10/12, self.buttons_width,
                                self.buttons_height, "Delete Table", self.gui.button_font, S.BUTTON_COLOR, S.BUTTON_HOVER_COLOR)
            self.start_button = Button(S.SCREEN_WIDTH*7/12, S.SCREEN_HEIGHT*10/12, self.buttons_width,
                                self.buttons_height, "Start Game", self.gui.button_font, S.BUTTON_COLOR, S.BUTTON_HOVER_COLOR)
            self.buttons = [self.start_button, self.delete_button]
        else:
            self.leave_button = Button(S.SCREEN_WIDTH*4/12, S.SCREEN_HEIGHT*10/12, self.buttons_width,
                                self.buttons_height, "Leave", self.gui.button_font, S.BUTTON_COLOR, S.BUTTON_HOVER_COLOR)
            self.buttons = [self.leave_button]

        self.rect_width = S.SCREEN_WIDTH*0.9
        self.rect_height = S.SCREEN_HEIGHT*0.65
        self.players_rect = pg.Rect(S.SCREEN_WIDTH*0.05, S.SCREEN_HEIGHT*0.15,
                                    self.rect_width, self.rect_height)
        self.pe_height = self.rect_height//4
        
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
                        if self.owner:
                            if self.delete_button.rect.collidepoint(event.pos):
                                self.gui.client.delete_table(self.table)
                            if self.start_button.rect.collidepoint(event.pos) and self.start_button.active:
                                self.gui.client.start_game(self.table)
                        else:
                            if self.leave_button.rect.collidepoint(event.pos):
                                self.gui.client.leave_table(self.table)
                                return

            self.draw()
            self.check_server()

    def draw(self):
        screen = self.gui.screen
        clock = self.gui.clock
        text_font = self.gui.text_font

        # Rysowanie menu
        screen.fill(S.BG_COLOR)

        # Rysowanie tytułu
        draw_text(screen, f"ID: {str(self.table.id)}     Name: {str(self.table.name)}", S.FONT_COLOR, S.SCREEN_WIDTH/2, S.SCREEN_HEIGHT*0.1, text_font, True)
        
        # Rysowanie przycisków
        for button in self.buttons:
            button.draw(screen)

        pg.draw.rect(screen, S.WHITE, self.players_rect, 2)

        if self.refresh_players:
            self.player_sprites = []
            for i, player in enumerate(self.table.players):
                player_rect = pg.Rect(self.players_rect.left, self.players_rect.top + i * self.pe_height,
                                    self.rect_width, self.pe_height)
                if self.players_rect.contains(player_rect):
                    player_sprite = PlayerItem(player, self.gui.xs_font, self.rect_width, self.pe_height)
                    player_sprite.rect = player_rect
                    self.player_sprites.append(player_sprite)
                
                if self.owner:
                    if len(self.table.players) > 1:
                        self.start_button.active = True
                    else:
                        self.start_button.active = False
            self.refresh_players = False

        for sprite in self.player_sprites:
            sprite.draw()
            screen.blit(sprite.surface, sprite.rect)

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
                self.table.players = []
                for i in range(len(splitted)//2):
                    id = splitted[i * 2]
                    name = splitted[i * 2 + 1]
                    self.table.players.append(Player(id, name, S.PLAYER_COLORS[len(self.table.players)]))
                self.refresh_players = True
            elif message == "DeletedTable":
                self.table_alive = False
            elif message == "StartGame":
                GameMenu(self.gui, self.table, self.owner)
                self.table_alive = False
            else:
                print(f"Unhandled message \"{message}\"") if S.DEBUG else None

            
    def close_program(self):
        return super().close_program()