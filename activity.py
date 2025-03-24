import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
import pygame

from sugar3.activity.activity import Activity
from sugar3.graphics.toolbarbox import ToolbarBox
from sugar3.activity.widgets import ActivityToolbarButton
from sugar3.activity.widgets import StopButton


import sugargame.canvas

import main


class FifteenPuzzle(Activity):
    def __init__(self, handle):
        Activity.__init__(self, handle)

        self.build_toolbar()
        self.game = main.Main(journal=True)

        # Build the Pygame canvas and start the game running
        # (self.game.run is called when the activity constructor
        # returns).
        self._pygamecanvas = sugargame.canvas.PygameCanvas(
            self, main=self.game.run, modules=[pygame.display]
        )
        self.game.set_canvas(self._pygamecanvas)

        # Note that set_canvas implicitly calls read_file when
        # resuming from the Journal.
        self.set_canvas(self._pygamecanvas)
        self._pygamecanvas.grab_focus()

    def build_toolbar(self):
        toolbar_box = ToolbarBox()
        self.set_toolbar_box(toolbar_box)
        toolbar_box.show()

        activity_button = ActivityToolbarButton(self)
        toolbar_box.toolbar.insert(activity_button, -1)
        activity_button.show()

        separator = Gtk.SeparatorToolItem()
        separator.props.draw = False
        separator.set_expand(True)
        toolbar_box.toolbar.insert(separator, -1)
        separator.show()

        stop_button = StopButton(self)
        toolbar_box.toolbar.insert(stop_button, -1)
        stop_button.show()
        self.show_all()

    def read_file(self, file_path):
        self.game.read_file(file_path)

    def write_file(self, file_path):
        self.game.write_file(file_path)

    def close(self):
        self.game.quit()