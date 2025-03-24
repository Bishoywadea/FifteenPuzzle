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
        # Draw the board
        self.board.draw()
        self.draw_help()

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
        if self.canvas is not None:
            self.canvas.grab_focus()
        
        self.help_pos = pg.Rect(
            (3 * config.WIDTH + config.BOARD_SIZE) // 4 - 40,
            (config.HEIGHT * 0.5 - config.BOARD_SIZE // 2) // 2 - 40,
            80,
            80,
        )
        self.question_text = pg.font.Font(None, 72).render("?", True, config.WHITE)


        self.reset_game()
        while self.running:
            if self.journal:
                # Pump GTK messages.
                while Gtk.events_pending():
                    Gtk.main_iteration()

            self.draw()
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