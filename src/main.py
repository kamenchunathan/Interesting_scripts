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
