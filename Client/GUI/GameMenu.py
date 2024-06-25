from GUI.UIComponents.TextFunctions import draw_text, render_text_scrolled
from GUI.UIComponents.Button import Button
from GUI.UIComponents.PlayerGameItem import PlayerGameItem
from GUI.UIComponents.TileGameItem import TileGameItem
from GUI.Menu import Menu
from Card import Card
from math import ceil
import pygame as pg
import SETTINGS as S

class GameMenu(Menu):
    def __init__(self, client, queue, clock, screen, table, owner):
        super().__init__(client, queue, clock, screen)   
        self.__table = table
        self.__my_move = owner
        self.__moving_player = 0
        self.__table_alive = True
        self.__show_move = True
        self.__dice_throw = True
        self.__attacked_players = 0
        self.__game_finished = False
        self.__given_rewards = False
        self.__current_card = Card(["NONE", "Error", "Something went wrong!"])
        self.__sorted_players = []

        # Players Rect
        self.__prect_width = S.SCREEN_WIDTH
        self.__prect_height = S.SCREEN_HEIGHT*0.3
        self.__players_rect = pg.Rect(0, S.SCREEN_HEIGHT*0.7,
                                    self.__prect_width, self.__prect_height)
        self.__player_width = self.__prect_width//4
        
        # Tiles Rect
        self.__trect_width = S.SCREEN_WIDTH
        self.__trect_height = S.SCREEN_HEIGHT - self.__prect_height
        self.__tiles_rect = pg.Rect(0, 0, self.__trect_width, self.__trect_height)
        self.__tile_width = self.__trect_width // S.TILES_ROW
        self.__tile_height = self.__trect_height // S.TILES_COL

        # Move Rect
        self.__mrect_width = self.__trect_width * 0.8
        self.__mrect_height = self.__trect_height * 0.8
        self.__card_rect = pg.Rect(S.SCREEN_WIDTH * 0.1, S.SCREEN_HEIGHT * 0.1,
                                self.__mrect_width//2, self.__mrect_height)
        self.__card_text_rect = pg.Rect(self.__card_rect.left + self.__mrect_width//2*0.1, self.__card_rect.top + self.__mrect_height*0.3,
                                      self.__mrect_width//2*0.8, self.__mrect_height*0.6)
        self.__choice_rect = pg.Rect(S.SCREEN_WIDTH * 0.1 + self.__mrect_width//2, S.SCREEN_HEIGHT * 0.1,
                                self.__mrect_width//2, self.__mrect_height)

        # Przyciski
        self.__move_button = Button((S.TILES_ROW - 1) * self.__tile_width + self.__tile_width * 0.1,
                                    (S.TILES_COL - 1) * self.__tile_height + self.__tile_height * 0.4,
                                    self.__tile_width * 0.8, self.__tile_height * 0.5, "Move", self._text_font)
        self._buttons.append(self.__move_button)

        # Scroll planszy
        self.__board_scroll = 0
        self.__board_button_scroll_speed = self.__tile_height
        self.__board_mouse_scroll_speed = self.__tile_height
        total_rows = ceil(S.TILE_COUNT / S.TILES_ROW)
        total_height = total_rows * self.__tile_height
        self.__board_scrollable_height = max(0, total_height - self.__trect_height)
        
        # Scroll tekstu na karcie
        self.__card_scroll = 0
        self.__card_text_padding = 10
        self.__card_line_spacing = 5
        self.__card_button_scroll_speed = 5
        self.__card_mouse_scroll_speed = self.__card_button_scroll_speed * 10

        # Dice button
        self.__dice_button = Button(self.__choice_rect.left + self.__mrect_width//2*0.1,
                                  self.__choice_rect.top + self.__mrect_height*0.5,
                                  self.__mrect_width//2*0.8, self.__mrect_height*0.3, "Throw", self._button_font)
        # Card buttons
        self.__confirm_button = Button(self.__choice_rect.left + self.__mrect_width//2*0.1,
                                  self.__choice_rect.top + self.__mrect_height*0.2,
                                  self.__mrect_width//2*0.8, self.__mrect_height*0.6, "Confirm", self._button_font)
        self.__player_one_button = Button(self.__choice_rect.left + self.__mrect_width//2*0.1,
                                  self.__choice_rect.top + self.__mrect_height*0.1,
                                  self.__mrect_width//2*0.8, self.__mrect_height*0.1, "Player One", self._button_font)
        self.__player_two_button = Button(self.__choice_rect.left + self.__mrect_width//2*0.1,
                                  self.__choice_rect.top + self.__mrect_height*0.3,
                                  self.__mrect_width//2*0.8, self.__mrect_height*0.1, "Player Two", self._button_font)
        self.__player_three_button = Button(self.__choice_rect.left + self.__mrect_width//2*0.1,
                                  self.__choice_rect.top + self.__mrect_height*0.5,
                                  self.__mrect_width//2*0.8, self.__mrect_height*0.1, "Player Three", self._button_font)
        self.__player_four_button = Button(self.__choice_rect.left + self.__mrect_width//2*0.1,
                                  self.__choice_rect.top + self.__mrect_height*0.7,
                                  self.__mrect_width//2*0.8, self.__mrect_height*0.1, "Player Four", self._button_font)
        self.__players_buttons = [self.__player_one_button, self.__player_two_button, self.__player_three_button, self.__player_four_button]
        for button in self.__players_buttons:
            button.set_active(False)
        self.__confirm_button.set_active(False)

        # Finish screen variables
        self.__finish_rect = pg.Rect(S.SCREEN_WIDTH * 0.1, S.SCREEN_HEIGHT * 0.1,
                                self.__mrect_width, self.__mrect_height)
        self.__end_game_button = Button(self.__finish_rect.left + self.__mrect_width*0.1,
                                  self.__choice_rect.top + self.__mrect_height*0.8,
                                  self.__mrect_width*0.8, self.__mrect_height*0.15, "Leave Game", self._button_font)
        self.__end_game_button.set_active(False)

        self.run()
        
    def run(self):
        # Główna pętla menu
        while self.__table_alive:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self._client.delete_table(self.__table)
                    self.close_program()
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.__move_button.check_click(event.pos):
                            self.__show_move = not self.__show_move
                        if self.__my_move and self.__dice_throw and self.__dice_button.check_click(event.pos):
                            self._client.throw_dice(self.__table)
                            self.__dice_button.set_active(False)
                        if self.__my_move and not self.__dice_throw:
                            if self.__confirm_button.check_click(event.pos):
                                self._client.card_confirm(self.__table, self.__current_card)
                                self.__confirm_button.set_active(False)
                            if self.__player_one_button.check_click(event.pos):
                                self._client.attack_player(self.__table, self.__table.get_player_id(0), self.__current_card)
                                self.__attack_player()
                            if self.__player_two_button.check_click(event.pos):
                                self._client.attack_player(self.__table, self.__table.get_player_id(1), self.__current_card)
                                self.__attack_player()
                            if self.__player_three_button.check_click(event.pos):
                                self._client.attack_player(self.__table, self.__table.get_player_id(2), self.__current_card)
                                self.__attack_player()
                            if self.__player_four_button.check_click(event.pos):
                                self._client.attack_player(self.__table, self.__table.get_player_id(3), self.__current_card)
                                self.__attack_player()
                        if self.__game_finished and self.__end_game_button.check_click(event.pos):
                            self._client.delete_table(self.__table)
                    elif event.button == 4:
                        if self.__show_move:
                            self.__card_scroll -= self.__card_mouse_scroll_speed if self.__card_scroll > 0 else 0
                        else:
                            self.__board_scroll -= self.__board_mouse_scroll_speed if self.__board_scroll > 0 else 0
                    elif event.button == 5:
                        if self.__show_move:
                            self.__card_scroll += self.__card_mouse_scroll_speed
                        else:
                            self.__board_scroll += self.__board_mouse_scroll_speed if self.__board_scroll < self.__board_scrollable_height else 0
            keys = pg.key.get_pressed()
            if keys[pg.K_UP]:
                if self.__show_move:
                    self.__card_scroll -= self.__card_button_scroll_speed if self.__card_scroll > 0 else 0
                else:
                    self.__board_scroll -= self.__board_button_scroll_speed if self.__board_scroll > 0 else 0
            elif keys[pg.K_DOWN]:
                if self.__show_move:
                    self.__card_scroll += self.__card_button_scroll_speed
                else:
                    self.__board_scroll += self.__board_button_scroll_speed if self.__board_scroll < self.__board_scrollable_height else 0

            self.draw()
            self.check_server()

    def __attack_player(self):
        self.__attacked_players += 1
        if self.__attacked_players >= self.__current_card.get_player_count():
            self._client.end_turn()

    def __draw_move(self):
        # Rysowanie karty
        pg.draw.rect(self._screen, S.BLACK, self.__card_rect)
        pg.draw.rect(self._screen, S.WHITE, self.__card_rect, 2)

        if not self.__dice_throw:
            draw_text(self._screen, self.__current_card.get_name(), S.WHITE,
                      self.__card_rect.left + self.__mrect_width//4,
                      self.__card_rect.top + self.__mrect_height*0.15,
                      self._text_font, True)
            render_text_scrolled(self._screen, self._ibox_font, self.__current_card.get_description(),
                                self.__card_scroll, S.WHITE, self.__card_line_spacing,
                                self.__card_text_rect, self.__card_text_padding)

        # Rysowanie możliwości
        pg.draw.rect(self._screen, S.BLACK, self.__choice_rect)
        pg.draw.rect(self._screen, S.WHITE, self.__choice_rect, 2)

        if self.__dice_throw:
            if self.__my_move:
                draw_text(self._screen, "Throw the dice:", S.WHITE, self.__choice_rect.left + self.__mrect_width//4,
                           self.__choice_rect.top + self.__mrect_height*0.15, self._text_font, True)
                self.__dice_button.draw(self._screen)
                mouse_pos = pg.mouse.get_pos()
                self.__dice_button.check_hover(mouse_pos)
            else:
                draw_text(self._screen, "Throwing the dice", S.WHITE, self.__choice_rect.left + self.__mrect_width//4,
                           self.__choice_rect.top + self.__mrect_height*0.15, self._text_font, True)
        else:
            if self.__my_move:
                card_type = self.__current_card.get_type()
                if card_type == "ATTACK":
                    mouse_pos = pg.mouse.get_pos()
                    for i in range(len(self.__table.get_players())):
                        self.__players_buttons[i].draw(self._screen)
                        self.__players_buttons[i].check_hover(mouse_pos)
                elif card_type == "GAIN":
                    self.__confirm_button.draw(self._screen)
                    self.__confirm_button.check_hover(pg.mouse.get_pos())
                elif card_type == "MOVE":
                    self.__confirm_button.draw(self._screen)
                    self.__confirm_button.check_hover(pg.mouse.get_pos())
            else:
                draw_text(self._screen, "Player is choosing", S.WHITE, self.__choice_rect.left + self.__mrect_width//4,
                           self.__choice_rect.top + self.__mrect_height*0.15, self._text_font, True)


    def __draw_finish_screen(self):
        pg.draw.rect(self._screen, S.BLACK, self.__finish_rect)
        pg.draw.rect(self._screen, S.WHITE, self.__finish_rect, 2)
        for i, player in enumerate(self.__sorted_players):
            text = f"{player.get_nickname()} - Gold: {player.get_gold()} - Goal: {player.get_progress()+1}"
            draw_text(self._screen, text, player.get_color(), self.__finish_rect.left + self.__mrect_width*0.5,
                      self.__finish_rect.top + self.__mrect_height*(0.1 + i * 0.2), self._text_font, True)
        self.__end_game_button.draw(self._screen)
        self.__end_game_button.check_hover(pg.mouse.get_pos())


    def draw(self):
        # Rysowanie menu
        self._screen.fill(S.BG_COLOR)


        self.__draw_game_map()
        self.__draw_players_info()

        if self.__game_finished:
            if not self.__given_rewards:
                for player in self.__table.get_players():
                    player.change_gold(player.get_progress())
                    self.__given_rewards = True
                    self.__sorted_players = sorted(self.__table.get_players(),
                                                key=lambda player: (player.get_gold(), player.get_progress()), reverse=True)

            self.__show_move = False
            for button in self._buttons:
                button.set_active(False)
            self.__end_game_button.set_active(True)
            self.__draw_finish_screen()
            

        if self.__show_move:
            self.__draw_move()

        # Rysowanie przycisków
        for button in self._buttons:
            button.draw(self._screen)

        # Odświeżenie ekranu
        pg.display.flip()
        self._clock.tick(S.FPS)

        # Sprawdzenie najechania myszką
        mouse_pos = pg.mouse.get_pos()
        for button in self._buttons:
            button.check_hover(mouse_pos)

    def __draw_game_map(self):
        # Wyrysowanie tile na górze
        for i in range(S.TILE_COUNT):
            tile_rect = pg.Rect(self.__tiles_rect.left + (i % S.TILES_ROW) * self.__tile_width,
                                self.__tiles_rect.top + (i // S.TILES_ROW) * self.__tile_height - self.__board_scroll,
                                self.__tile_width, self.__tile_height)
            if self.__tiles_rect.contains(tile_rect):
                tile_sprite = TileGameItem(self.__tile_width, self.__tile_height)
                tile_sprite.set_rect_topleft((self.__tiles_rect.left + (i % S.TILES_ROW) * self.__tile_width,
                                            self.__tiles_rect.top + (i // S.TILES_ROW) * self.__tile_height - self.__board_scroll))
                players = []
                for player in self.__table.get_players():
                    if player.get_progress() == i:
                        players.append(player)
                tile_sprite.draw(players)
                self._screen.blit(tile_sprite.get_surface(), tile_sprite.get_rect().topleft)
                pg.draw.rect(self._screen, S.TILE_BORDER_COLOR, tile_sprite.get_rect(), 2)

    def __draw_players_info(self):
        # Wyrysowanie graczy na dole ekranu
        pg.draw.rect(self._screen, S.WHITE, self.__players_rect, 2)
        for i, player in enumerate(self.__table.get_players()):
            player_rect = pg.Rect(self.__players_rect.left + i * self.__player_width, self.__players_rect.top,
                                self.__player_width, self.__prect_height)
            player_sprite = PlayerGameItem(player, self._text_font, self.__player_width, self.__prect_height)
            player_sprite.set_rect(player_rect)
            player_sprite.draw()
            self._screen.blit(player_sprite.get_surface(), player_sprite.get_rect())
            pg.draw.rect(self._screen, S.WHITE, player_sprite.get_rect(), 2)

    def check_server(self):
        while not self._message_queue.empty():
            message: str = self._message_queue.get_nowait()
            if message.startswith("PlayersList"):
                splitted = message.split(";")
                splitted = splitted[1:]
                players = self.__table.get_players()
                for player in players:
                    player.set_found(False)

                for i in range(len(splitted)//2):
                    id = splitted[i * 2]
                    for player in players:
                        if id == player.get_id():
                            player.set_found(True)

                for player in players:
                    if not player.get_found():
                        self.__table.remove_player(player)
            elif message == "DeletedTable":
                self.__table_alive = False
            elif message.startswith("DiceThrown"):
                _, player_id, move = message.split(";")
                for player in self.__table.get_players():
                    if player.get_id() == player_id:
                        self.__game_finished = player.move_player(int(move))
                self.__dice_throw = False
            elif message.startswith("Card"):
                splitted = message.split(";")
                self.__current_card = Card(splitted[1:])

                card_type = self.__current_card.get_type()
                if card_type == "GAIN" or card_type == "MOVE":
                    self.__confirm_button.set_active(True)
                elif card_type == "ATTACK":
                    self.__attacked_players = 0
                    for i in range(len(self.__table.get_players())):
                        self.__players_buttons[i].set_active(True)

            elif message.startswith("ChangeMaterial"):
                _, player_id, material, count = message.split(";")
                
                for player in self.__table.get_players():
                    if player.get_id() == player_id:
                        if material == "Progress":
                            self.__game_finished = player.move_player(int(count))
                        elif material == "Gold":
                            player.change_gold(int(count))
            elif message == "NextTurn":
                self.__current_card.clear_card()
                
                self.__confirm_button.set_active(False)
                for button in self.__players_buttons:
                    button.set_active(False)

                self.__moving_player += 1
                if self.__moving_player == len(self.__table.get_players()):
                    self.__moving_player = 0
                if self.__table.get_players()[self.__moving_player].get_id() == self._client.get_id():
                    self.__my_move = True
                    self.__dice_button.set_active(True)
                else:
                    self.__my_move = False

                self.__dice_throw = True
            else:
                print(f"Unhandled message \"{message}\"") if S.DEBUG else None

            
    def close_program(self):
        return super().close_program()