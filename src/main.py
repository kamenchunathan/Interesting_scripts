from __future__ import annotations

from typing import Callable

from bitarray import bitarray
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Rectangle, Line
from kivy.properties import NumericProperty
# ################################################################
#                         Game constants
# ################################################################
from kivy.uix.widget import Widget

DEFAULT_WORLD_SIZE = 40
MAX_WORLD_SIZE = 100  # TODO: Calculate as a function of the limits of the hardware


# ################################################################
#                       Game Logic and rendering
# ################################################################

class State:
    """
    Container class that will store the state of all the cells in the world at a given instance
    in a dense configuration (bit array) with live cells stored as 1 and dead cells stored as 0
    """

    def __init__(self, size):
        self.size = size
        self._data = bitarray(self.size ** 2)
        self._data.setall(False)

    def __getitem__(self, *key: tuple):
        return self._data[key[0] * self.size + key[1]]

    def __setitem__(self, key: tuple, value: bool):
        self._data[key[0] * self.size + key[1]] = value

    def __iter__(self):
        for i in range(self.size):
            for j in range(self.size):
                yield self[i, j]

    def total_alive_neighbours(self, x, y) -> int:
        live_neighbours = 0
        if x > 0 and y > 0:
            if self[x - 1, y - 1]:
                live_neighbours += 1
        if y > 0:
            if self[x, y - 1]:
                live_neighbours += 1
        if x < self.size and y > 0:
            if self[x + 1, y - 1]:
                live_neighbours += 1
        if x > 0:
            if self[x - 1, y]:
                live_neighbours += 1
        if x < self.size:
            if self[x + 1, y]:
                live_neighbours += 1
        if x > 0 and y < self.size:
            if self[x - 1, y + 1]:
                live_neighbours += 1
        if y < self.size:
            if self[x, y + 1]:
                live_neighbours += 1
        if x < self.size and y < self.size:
            if self[x + 1, y + 1]:
                live_neighbours += 1

        return live_neighbours

    def apply_rule_set(self, rule_set: Callable[[int], bool]) -> State:
        """
        Applies a set of rules that transforms the state and returns the new state

        :param self:
        :param rule_set: an array of functions that is called for every cell in the
        :return: a new state that is the product of the application of the provided rule set
        """
        next_state = State(self.size)
        for i in range(self.size):
            for j in range(self.size):
                next_state[i, j] = rule_set(self.total_alive_neighbours(i, j))
        return next_state


class World(Widget):
    def __init__(self, world_size, **kwargs):
        super().__init__(**kwargs)
        self.world_size = world_size

        self.render()

    def render(self, *args, **kwargs):
        """
        Renders the world according to its current state using the widget canvas
        :return: None
        """
        with self.canvas:
            for i in range(self.world_size):  # horizontal axis
                for j in range(self.world_size):  # vertical axis
                    cell_coord = i * self.cell_size[0], j * self.cell_size[1]

                    # Draw cell
                    Color(1, 1, 1)
                    Rectangle(size=self.cell_size, pos=(cell_coord[0], cell_coord[1]))

                    # Draw the cell border
                    Color(0, 0, 0)
                    Line(
                        points=[cell_coord[0], cell_coord[1],
                                cell_coord[0] + self.cell_size[0], cell_coord[1],
                                cell_coord[0] + self.cell_size[0], cell_coord[1] + self.cell_size[1],
                                cell_coord[0], cell_coord[1] + self.cell_size[1],
                                ],
                        width=0.3,
                        cap='square',
                        joint='miter',
                        close=True)

    @property
    def cell_size(self):
        """
        :return: the size of a single cell calculated based on the screen divided by the number of cells in the world
        """
        return Window.size[0] / self.world_size, Window.size[1] / self.world_size


class GameOfLife(App):
    """
    Creates a world of the set size and calls its render function
    """

    # The world size is only a single constant because in this simple iteration of the game of life simulation
    # the world is square.
    # This might be change later to support world sizes of different length and width dimensions
    world_size = NumericProperty(DEFAULT_WORLD_SIZE)
    time_step = NumericProperty(2)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.world = None

    def build(self):
        self.world = World(self.world_size)
        return self.world

    def on_start(self):
        Clock.schedule_interval(self.world.render, self.time_step)


if __name__ == '__main__':
    GameOfLife().run()
