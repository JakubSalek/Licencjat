from GUI.UIComponents.TextFunctions import draw_text
from GUI.UIComponents.Button import Button
from GUI.UIComponents.PlayerBanerItem import PlayerBanerItem
from GUI.Menu import Menu
from GUI.GameMenu import GameMenu
import pygame as pg
import SETTINGS as S
from Player import Player

class TableMenu(Menu):
    def __init__(self, client, queue, clock, screen, table, owner):
        super().__init__(client, queue, clock, screen)   
        self.__table = table
        self.__owner = owner
        self.__table_alive = True
        self.__buttons = []
        self.__refresh_players = True
        self.__player_sprites = []

        buttons_width = S.SCREEN_WIDTH * 4/12
        buttons_height = S.SCREEN_HEIGHT/12

        if self.__owner:
            self.__delete_button = Button(S.SCREEN_WIDTH*1/12, S.SCREEN_HEIGHT*10/12, buttons_width,
                                        buttons_height, "Delete Table", self._button_font)
            self.__start_button = Button(S.SCREEN_WIDTH*7/12, S.SCREEN_HEIGHT*10/12, buttons_width,
                                        buttons_height, "Start Game", self._button_font)
            self.__buttons = [self.__start_button, self.__delete_button]
        else:
            self.__leave_button = Button(S.SCREEN_WIDTH*4/12, S.SCREEN_HEIGHT*10/12, buttons_width,
                                        buttons_height, "Leave", self._button_font)
            self.__buttons = [self.__leave_button]

        self.__rect_width = S.SCREEN_WIDTH*0.9
        self.__rect_height = S.SCREEN_HEIGHT*0.65
        self.__players_rect = pg.Rect(S.SCREEN_WIDTH*0.05, S.SCREEN_HEIGHT*0.15,
                                    self.__rect_width, self.__rect_height)
        self.__pe_height = self.__rect_height//4
        
        self.run()
        
    def run(self):
        # Główna pętla menu
        while self.__table_alive:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    if self.__owner:
                        self._client.delete_table(self.__table)
                    else:
                        self._client.leave_table(self.__table)
                    self.close_program()
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.__owner:
                            if self.__delete_button.check_click(event.pos):
                                self._client.delete_table(self.__table)
                            if self.__start_button.check_click(event.pos):
                                self._client.start_game(self.__table)
                        else:
                            if self.__leave_button.check_click(event.pos):
                                self._client.leave_table(self.__table)
                                return

            self.draw()
            self.check_server()

    def draw(self):
        # Rysowanie menu
        self._screen.fill(S.BG_COLOR)

        # Rysowanie tytułu
        table_title = f"ID: {str(self.__table.get_id())}     Name: {str(self.__table.get_name())}"
        draw_text(self._screen, table_title, S.FONT_COLOR, S.SCREEN_WIDTH/2,
                   S.SCREEN_HEIGHT*0.1, self._text_font, True)
        
        # Rysowanie przycisków
        for button in self.__buttons:
            button.draw(self._screen)

        pg.draw.rect(self._screen, S.WHITE, self.__players_rect, 2)

        if self.__refresh_players:
            self.__player_sprites = []
            for i, player in enumerate(self.__table.get_players()):
                player_rect = pg.Rect(self.__players_rect.left, self.__players_rect.top + i * self.__pe_height,
                                    self.__rect_width, self.__pe_height)
                if self.__players_rect.contains(player_rect):
                    player_sprite = PlayerBanerItem(player, self._text_font, self.__rect_width, self.__pe_height)
                    player_sprite.set_rect(player_rect)
                    self.__player_sprites.append(player_sprite)
                
                if self.__owner:
                    if len(self.__table.get_players()) > 1:
                        self.__start_button.set_active(True)
                    else:
                        self.__start_button.set_active(False)
            self.__refresh_players = False

        for sprite in self.__player_sprites:
            sprite.draw()
            self._screen.blit(sprite.get_surface(), sprite.get_rect())

        # Odświeżenie ekranu
        pg.display.flip()
        self._clock.tick(S.FPS)

        # Sprawdzenie najechania myszką
        mouse_pos = pg.mouse.get_pos()
        for button in self.__buttons:
            button.check_hover(mouse_pos)

    def check_server(self):
        while not self._message_queue.empty():
            message: str = self._message_queue.get_nowait()
            if message.startswith("PlayersList"):
                splitted = message.split(";")
                splitted = splitted[1:]
                self.__table.clear_players()
                for i in range(len(splitted)//2):
                    id = splitted[i * 2]
                    name = splitted[i * 2 + 1]
                    self.__table.add_player(Player(id, name, S.PLAYER_COLORS[len(self.__table.get_players())]))
                self.__refresh_players = True
            elif message == "DeletedTable":
                self.__table_alive = False
            elif message == "StartGame":
                GameMenu(self._client, self._message_queue, self._clock, self._screen, self.__table, self.__owner)
                self.__table_alive = False
            else:
                print(f"Unhandled message \"{message}\"") if S.DEBUG else None

    def close_program(self):
        return super().close_program()