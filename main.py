import pygame as pg
import sys
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from gettext import gettext as _

# Configuration constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Main:
    def __init__(self, journal=True):
        self.journal = journal
        self.running = True
        self.screen = None
        self.font = None

    def set_canvas(self, canvas):
        self.screen = canvas
        pg.display.set_caption(_("Hello World App"))

    def quit(self):
        self.running = False

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()

    def draw(self):
        self.screen.fill(WHITE)
        text = self.font.render(_("Hello, World!"), True, BLACK)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(text, text_rect)
        pg.display.update()

    def run(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT), pg.RESIZABLE)
        self.font = pg.font.Font(None, 72)

        if self.screen is not None:
            self.screen.fill(WHITE)
            pg.display.flip()

        while self.running:
            if self.journal:
                while Gtk.events_pending():
                    Gtk.main_iteration()

            self.check_events()
            self.draw()
            pg.time.Clock().tick(30)

        pg.quit()
        sys.exit(0)

if __name__ == "__main__":
    main = Main(journal=False)
    main.run()
