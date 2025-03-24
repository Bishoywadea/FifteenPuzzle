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

    def draw(self):
        config.WIN.fill(config.BLACK)
        # Draw the board
        self.board.draw()
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