import math
from Card import Card
from GUI.Menu import Menu
from GUI.UIComponents import draw_text, Button, render_text_scrolled
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
        draw_text(self.surface, f"Goal: {self.player.progress+1}/{S.TILE_COUNT}", S.BLACK, self.swidth//2, self.sheight * 0.75, self.font, True)


class GameMenu(Menu):
    def __init__(self, gui, table, is_owner):
        super().__init__(gui)   
        self.table = table
        self.owner = is_owner
        self.my_move = is_owner
        self.moving_player = 0
        self.table_alive = True
        self.show_move = True
        self.dice_throw = True
        self.game_finished = False
        self.given_rewards = False
        self.current_card = Card(["NONE", "Error", "Something went wrong!"])
        self.buttons = []
        self.sorted_players = []

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
        self.mrect_width = self.trect_width * 0.8
        self.mrect_height = self.trect_height * 0.8
        self.card_rect = pg.Rect(S.SCREEN_WIDTH * 0.1, S.SCREEN_HEIGHT * 0.1,
                                self.mrect_width//2, self.mrect_height)
        self.card_text_rect = pg.Rect(self.card_rect.left + self.mrect_width//2*0.1, self.card_rect.top + self.mrect_height*0.3,
                                      self.mrect_width//2*0.8, self.mrect_height*0.6)
        self.choice_rect = pg.Rect(S.SCREEN_WIDTH * 0.1 + self.mrect_width//2, S.SCREEN_HEIGHT * 0.1,
                                self.mrect_width//2, self.mrect_height)

        # Przyciski
        self.move_button = Button((S.TILES_ROW - 1) * self.tile_width + self.tile_width * 0.1,
                                    (S.TILES_COL - 1) * self.tile_height + self.tile_height * 0.4,
                                    self.tile_width * 0.8, self.tile_height * 0.5, "Move", self.gui.xs_font)
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

        # Dice button
        self.dice_button = Button(self.choice_rect.left + self.mrect_width//2*0.1,
                                  self.choice_rect.top + self.mrect_height*0.5,
                                  self.mrect_width//2*0.8, self.mrect_height*0.3, "Throw", self.gui.button_font)
        # Card buttons
        self.confirm_button = Button(self.choice_rect.left + self.mrect_width//2*0.1,
                                  self.choice_rect.top + self.mrect_height*0.2,
                                  self.mrect_width//2*0.8, self.mrect_height*0.6, "Confirm", self.gui.button_font)
        self.player_one_button = Button(self.choice_rect.left + self.mrect_width//2*0.1,
                                  self.choice_rect.top + self.mrect_height*0.1,
                                  self.mrect_width//2*0.8, self.mrect_height*0.1, "Player One", self.gui.button_font)
        self.player_two_button = Button(self.choice_rect.left + self.mrect_width//2*0.1,
                                  self.choice_rect.top + self.mrect_height*0.3,
                                  self.mrect_width//2*0.8, self.mrect_height*0.1, "Player Two", self.gui.button_font)
        self.player_three_button = Button(self.choice_rect.left + self.mrect_width//2*0.1,
                                  self.choice_rect.top + self.mrect_height*0.5,
                                  self.mrect_width//2*0.8, self.mrect_height*0.1, "Player Three", self.gui.button_font)
        self.player_four_button = Button(self.choice_rect.left + self.mrect_width//2*0.1,
                                  self.choice_rect.top + self.mrect_height*0.7,
                                  self.mrect_width//2*0.8, self.mrect_height*0.1, "Player Four", self.gui.button_font)
        self.players_buttons = [self.player_one_button, self.player_two_button, self.player_three_button, self.player_four_button]
        for button in self.players_buttons:
            button.active = False


        # Finish screen variables
        self.finish_rect = pg.Rect(S.SCREEN_WIDTH * 0.1, S.SCREEN_HEIGHT * 0.1,
                                self.mrect_width, self.mrect_height)
        self.end_game_button = Button(self.finish_rect.left + self.mrect_width*0.1,
                                  self.choice_rect.top + self.mrect_height*0.8,
                                  self.mrect_width*0.8, self.mrect_height*0.15, "Leave Game", self.gui.button_font)
        self.end_game_button.active = False


        self.run()
        
    def run(self):
        # Główna pętla menu
        while self.table_alive:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.gui.client.delete_table(self.table)
                    self.close_program()
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.move_button.rect.collidepoint(event.pos):
                            self.show_move = not self.show_move
                        if self.my_move and self.dice_throw and self.dice_button.active and self.dice_button.rect.collidepoint(event.pos):
                            self.gui.client.throw_dice(self.table)
                            self.dice_button.active = False
                        if self.my_move and not self.dice_throw and self.confirm_button.active and self.confirm_button.rect.collidepoint(event.pos):
                            self.gui.client.card_confirm(self.table, self.current_card)
                            self.confirm_button.active = False
                        if self.my_move and not self.dice_throw and self.player_one_button.active and self.player_one_button.rect.collidepoint(event.pos):
                            
                            self.player_one_button.active = False
                        if self.my_move and not self.dice_throw and self.player_two_button.active and  self.player_two_button.rect.collidepoint(event.pos):
                            
                            self.player_two_button.active = False
                        if self.my_move and not self.dice_throw and self.player_three_button.active and  self.player_three_button.rect.collidepoint(event.pos):
                            
                            self.player_three_button.active = False
                        if self.my_move and not self.dice_throw and self.player_four_button.active and  self.player_four_button.rect.collidepoint(event.pos):
                            
                            self.player_four_button.active = False
                        if self.game_finished and self.end_game_button.active and self.end_game_button.rect.collidepoint(event.pos):
                            if self.owner:
                                self.gui.client.delete_table(self.table)
                            else:
                                self.gui.client.leave_table(self.table)
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

        if not self.dice_throw:
            draw_text(screen, self.current_card.name, S.WHITE,
                      self.card_rect.left + self.mrect_width//4,
                      self.card_rect.top + self.mrect_height*0.15,
                      self.gui.text_font, True)
            render_text_scrolled(screen, self.gui.ibox_font, self.current_card.description,
                                self.card_scroll, S.WHITE, self.card_line_spacing,
                                self.card_text_rect, self.card_text_padding)

        # Rysowanie możliwości
        pg.draw.rect(screen, S.BLACK, self.choice_rect)
        pg.draw.rect(screen, S.WHITE, self.choice_rect, 2)

        if self.dice_throw:
            if self.my_move:
                draw_text(screen, "Throw the dice:", S.WHITE, self.choice_rect.left + self.mrect_width//4,
                           self.choice_rect.top + self.mrect_height*0.15, self.gui.text_font, True)
                self.dice_button.draw(screen)
                mouse_pos = pg.mouse.get_pos()
                self.dice_button.check_hover(mouse_pos)
            else:
                draw_text(screen, "Throwing the dice", S.WHITE, self.choice_rect.left + self.mrect_width//4,
                           self.choice_rect.top + self.mrect_height*0.15, self.gui.text_font, True)
        else:
            if self.my_move:
                card_type = self.current_card.card_type
                if card_type == "ATTACK":
                    mouse_pos = pg.mouse.get_pos()
                    for button in self.players_buttons:
                        button.draw(screen)
                        button.check_hover(mouse_pos)
                elif card_type == "GAIN":
                    self.confirm_button.draw(screen)
                    mouse_pos = pg.mouse.get_pos()
                    self.confirm_button.check_hover(mouse_pos)
                elif card_type == "MOVE":
                    self.confirm_button.draw(screen)
                    mouse_pos = pg.mouse.get_pos()
                    self.confirm_button.check_hover(mouse_pos)
            else:
                draw_text(screen, "Player is choosing", S.WHITE, self.choice_rect.left + self.mrect_width//4,
                           self.choice_rect.top + self.mrect_height*0.15, self.gui.text_font, True)


    def draw_finish_screen(self, screen):
        pg.draw.rect(screen, S.BLACK, self.finish_rect)
        pg.draw.rect(screen, S.WHITE, self.finish_rect, 2)

        for i, player in enumerate(self.sorted_players):
            text = f"{player.nickname} - Gold: {player.gold} - Goal: {player.progress}"
            draw_text(screen, text, player.color, self.finish_rect.left + self.mrect_width*0.5,
                      self.finish_rect.top + self.mrect_height*(0.1 + i * 0.2), self.gui.text_font, True)
            
        self.end_game_button.draw(screen)
        mouse_pos = pg.mouse.get_pos()
        self.end_game_button.check_hover(mouse_pos)


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

        if self.game_finished:
            if not self.given_rewards:
                for player in self.table.players:
                    player.change_gold(player.progress)
                    self.given_rewards = True

            self.sorted_players = sorted(self.table.players, key=lambda player: (player.gold, player.progress), reverse=True)

            self.show_move = False
            for button in self.buttons:
                button.active = False
            self.end_game_button.active = True
            self.draw_finish_screen(screen)
            

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
            elif message.startswith("DiceThrown"):
                _, player_id, move = message.split(";")
                for player in self.table.players:
                    if player.id == player_id:
                        self.game_finished = player.move_player(int(move))
                self.dice_throw = False
            elif message.startswith("Card"):
                splitted = message.split(";")
                self.current_card = Card(splitted[1:])

                if self.current_card.card_type == "GAIN" or self.current_card.card_type == "MOVE":
                    self.confirm_button.active = True
                elif self.current_card.card_type == "ATTACK":
                    for button in self.players_buttons:
                        button.active = True

            elif message.startswith("ChangeMaterial"):
                _, player_id, material, count = message.split(";")
                
                for player in self.table.players:
                    if player.id == player_id:
                        if material == "Progress":
                            self.game_finished = player.move_player(int(count))
                        elif material == "Gold":
                            player.change_gold(int(count))
            elif message == "NextTurn":
                self.current_card.clear_card()
                
                self.moving_player += 1
                if self.moving_player == len(self.table.players):
                    self.moving_player = 0
                if self.table.players[self.moving_player].id == self.gui.client.id:
                    self.my_move = True
                    self.dice_button.active = True
                else:
                    self.my_move = False

                self.dice_throw = True
            else:
                print(f"Unhandled message \"{message}\"") if S.DEBUG else None

            
    def close_program(self):
        return super().close_program()