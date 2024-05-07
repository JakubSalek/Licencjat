from GUI.UIComponents import draw_text, Button
import pygame as pg
from GUI.Menu import Menu
import SETTINGS as S

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
    def __init__(self, gui, table):
        super().__init__(gui)   
        self.table = table
        self.owner = self.table.players[0].id == self.gui.client.id
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
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.close_program()
                    # TODO informacja ze opuszcza stolik
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.owner:
                            if self.delete_button.rect.collidepoint(event.pos):
                                # TODO usuniecie stolika i cofniecie wszystkich do menu
                                pass
                            if self.start_button.rect.collidepoint(event.pos):
                                # TODO rozpoczecie rozgrywki
                                pass
                        else:
                            if self.leave_button.rect.collidepoint(event.pos):
                                # TODO cofniecie i poinformowanie reszty o zmianie
                                pass

            self.draw()
            self.check_server()

    def draw(self):
        self.reinitialize_menu() if self.reinitialize else None
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
            button.check_hover(mouse_pos)

    def check_server(self):
        while not self.gui.message_queue.empty():
            message = self.gui.message_queue.get_nowait()
            
    def close_program(self):
        return super().close_program()