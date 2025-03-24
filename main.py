import pygame as pg
import sys
import random
import gi
from board import Board
import math

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from gettext import gettext as _

import config

# The main controller
class Main:
    def __init__(self, journal=True):
        self.journal = journal
        self.running = True
        self.canvas = None
        self.moves = 0
        self.show_help = False
        self.help_img = None  # We'll need to create a help image for 15 puzzle
        self.board = None
        self.solved = False
        self.fancy_button_anim = 0  # Animation counter for the fancy button

    def set_canvas(self, canvas):
        self.canvas = canvas
        pg.display.set_caption(_("15 Puzzle"))

    def quit(self):
        self.running = False

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            if event.type == pg.VIDEORESIZE:
                pg.display.set_mode(event.size, pg.RESIZABLE)
                break
            if event.type == pg.MOUSEBUTTONUP:
                if self.help_pos.collidepoint(pg.mouse.get_pos()):
                    self.show_help = not self.show_help
                if self.show_help:
                    break
                if self.canvas is not None:
                    self.canvas.grab_focus()
                if not self.solved and self.board.handle_click(pg.mouse.get_pos()):
                    self.moves += 1
                if self.reset_rect.collidepoint(pg.mouse.get_pos()):
                    self.reset_game()
                # Check for fancy button click when puzzle is solved
                if self.solved and self.fancy_button_rect.collidepoint(pg.mouse.get_pos()):
                    self.reset_game()
                

    def draw_help(self):
        # Draw the help button
        pg.draw.circle(
            config.WIN,
            config.GREY,
            self.help_pos.center,
            40,
        )
        
        if self.show_help:
            # Draw the X button to close help
            width = self.close_text.get_width()
            height = self.close_text.get_height()
            close_rect = (
                self.help_pos.centerx - width // 2,
                self.help_pos.centery - height // 2
            )
            config.WIN.blit(
                self.close_text, close_rect
            )
            
            # Calculate the dimensions for help panel based on text content
            max_text_width = max(text.get_width() for text in self.help_text)
            total_text_height = sum(text.get_height() for text in self.help_text)
            spacing = 40  # Space between lines
            
            # Calculate padding
            horizontal_padding = 50
            vertical_padding = 60
            
            # Calculate help panel dimensions
            help_width = max_text_width + (horizontal_padding * 2)
            help_height = total_text_height + ((len(self.help_text) - 1) * spacing) + (vertical_padding * 2)
            
            # Center the help panel
            help_x = (config.WIDTH - help_width) // 2
            help_y = (config.HEIGHT - help_height) // 2
            
            # Draw the help panel background
            pg.draw.rect(
                config.WIN,
                config.GREY,
                pg.Rect(
                    help_x,
                    help_y,
                    help_width,
                    help_height,
                ),
                border_radius=15  # Optional: rounded corners
            )
            
            # Draw each line of help text
            y_offset = help_y + vertical_padding
            for text in self.help_text:
                text_x = (config.WIDTH - text.get_width()) // 2
                config.WIN.blit(text, (text_x, y_offset))
                y_offset += text.get_height() + spacing
                
        else:
            # Draw the question mark CENTERED ON the help button
            q_width = self.question_text.get_width()
            q_height = self.question_text.get_height()
            
            # Calculate position to center the question mark on the help button
            q_x = self.help_pos.centerx - q_width // 2
            q_y = self.help_pos.centery - q_height // 2
            
            config.WIN.blit(self.question_text, (q_x, q_y))
        
    def draw(self):
        config.WIN.fill(config.BLACK)
        heading_w = self.heading.get_width()
        heading_h = self.heading.get_height()
        heading_rect = (
            (config.WIDTH - heading_w) // 2,
            (config.HEIGHT * 0.5 - config.BOARD_SIZE // 2 - heading_h) // 2,
        )
        config.WIN.blit(
            self.heading, heading_rect
        )
        
        # Draw move counter
        moves_text = self.font.render(_("Moves: ") + str(self.moves), True, config.WHITE)
        config.WIN.blit(
            moves_text,
            (
                (config.WIDTH - config.BOARD_SIZE) // 4,
                config.HEIGHT // 2 - config.BOARD_SIZE // 4,
            ),
        )

        # Draw the board
        self.board.draw()
        
        # Draw help button
        self.draw_help()
        
        # If puzzle is not solved, draw regular reset button
        if not self.solved:
            pg.draw.rect(config.WIN, config.GREY, self.reset_rect)
            pg.draw.circle(
                config.WIN,
                config.GREY,
                (int(self.reset_rect.x), int(self.reset_rect.centery)),
                self.reset_rect.height // 2,
            )
            pg.draw.circle(
                config.WIN,
                config.GREY,
                (int(self.reset_rect.right), int(self.reset_rect.centery)),
                self.reset_rect.height // 2,
            )
            config.WIN.blit(
                self.reset_text,
                (
                    config.WIDTH / 2 - self.reset_text.get_width() / 2,
                    config.HEIGHT - self.reset_text.get_height() - 70,
                ),
            )
        
        # If puzzle is solved, show congratulations and fancy button
        if self.solved:
            # Create a semi-transparent overlay
            overlay = pg.Surface((config.WIDTH, config.HEIGHT), pg.SRCALPHA)
            overlay.fill((0, 0, 0, 128))
            config.WIN.blit(overlay, (0, 0))
            
            # Draw congratulations text
            congrats_text = self.congratulation_font.render(_("Puzzle Solved!"), True, config.ORANGE)
            moves_info = self.font.render(_("Completed in ") + str(self.moves) + _(" moves!"), True, config.WHITE)
            
            config.WIN.blit(
                congrats_text,
                (
                    config.WIDTH // 2 - congrats_text.get_width() // 2,
                    config.HEIGHT // 2 - congrats_text.get_height() - 100,
                ),
            )
            
            config.WIN.blit(
                moves_info,
                (
                    config.WIDTH // 2 - moves_info.get_width() // 2,
                    config.HEIGHT // 2 - moves_info.get_height(),
                ),
            )
            
            # Draw the fancy button
            self.draw_fancy_button()
            
        pg.display.update()

    def reset_game(self):
        self.board = Board(self, (config.WIDTH / 2, config.HEIGHT / 2))
        self.moves = 0
        self.solved = False

    # The main loop
    def run(self):
        for event in pg.event.get():
            if event.type == pg.VIDEORESIZE:
                pg.display.set_mode(event.size, pg.RESIZABLE)
                break
        config.init()
        pg.font.init()
        self.heading = pg.font.Font(None, 96).render(
            _("15 Puzzle"),
            True,
            config.WHITE
        )
        self.reset_text = pg.font.Font(None, 56).render(
            _("New Game"),
            True,
            config.WHITE
        )
        self.question_text = pg.font.Font(None, 72).render("?", True, config.WHITE)
        self.close_text = pg.font.Font(None, 64).render("X", True, config.WHITE)
        self.help_text = [
            pg.font.Font(None, 36).render(
                i,
                True,
                config.WHITE,
            )
            for i in (
                _("Slide the numbered tiles to arrange them in order."),
                _("Click a tile adjacent to the empty space to move it."),
                _("The goal is to arrange the tiles from 1 to 15 with"),
                _("the empty space in the bottom right corner."),
            )
        ]
        self.help_pos = pg.Rect(
            (3 * config.WIDTH + config.BOARD_SIZE) // 4 - 40,
            (config.HEIGHT * 0.5 - config.BOARD_SIZE // 2) // 2 - 40,
            80,
            80,
        )
        self.reset_rect = pg.Rect(
            config.WIDTH / 2 - self.reset_text.get_width() / 2,
            config.HEIGHT - self.reset_text.get_height() - 80,
            self.reset_text.get_width(),
            self.reset_text.get_height() + 20,
        )
        self.font = pg.font.Font(None, 72)
        self.fancy_font = pg.font.Font(None, 64)
        self.congratulation_font = pg.font.Font(None, 120)
        self.fancy_button_rect = pg.Rect(0, 0, 0, 0)  # Initialize with dummy values

        if self.canvas is not None:
            self.canvas.grab_focus()

        self.reset_game()
        self.clock = pg.time.Clock()
        while self.running:
            if self.journal:
                # Pump GTK messages.
                while Gtk.events_pending():
                    Gtk.main_iteration()

            self.check_events()
            self.draw()
            self.clock.tick(config.FPS)
        pg.display.quit()
        pg.quit()
        sys.exit(0)


# Test if the script is directly ran
if __name__ == "__main__":
    pg.init()
    # Set your desired width and height
    info = pg.display.Info()
    screen_width, screen_height = info.current_w, info.current_h
    # Set the display mode with the specified width and height
    screen = pg.display.set_mode((screen_width, screen_height), pg.FULLSCREEN)
    main = Main(journal=False)
    main.run()