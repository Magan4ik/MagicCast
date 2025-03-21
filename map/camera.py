import pyglet

from base_classes.coordinate_object import CoordinateObject


class Camera:
    """ A simple 2D camera that contains the speed and offset."""

    def __init__(self, window: pyglet.window.Window, scroll_speed=1, min_zoom=1, max_zoom=4):
        assert min_zoom <= max_zoom, "Minimum zoom must not be greater than maximum zoom"
        self._window = window
        self.scroll_speed = scroll_speed
        self.max_zoom = max_zoom
        self.min_zoom = min_zoom
        self.offset_x = 0
        self.offset_y = 0
        self._zoom = max(min(1, self.max_zoom), self.min_zoom)

    @property
    def zoom(self):
        return self._zoom

    @zoom.setter
    def zoom(self, value):
        """ Here we set zoom, clamp value to minimum of min_zoom and max of max_zoom."""
        self._zoom = max(min(value, self.max_zoom), self.min_zoom)

    @property
    def position(self):
        """Query the current offset."""
        return self.offset_x, self.offset_y

    @position.setter
    def position(self, value):
        """Set the scroll offset directly."""
        self.offset_x, self.offset_y = value

    def move(self, axis_x, axis_y):
        """ Move axis direction with scroll_speed.
            Example: Move left -> move(-1, 0)
         """
        self.offset_x += self.scroll_speed * axis_x
        self.offset_y += self.scroll_speed * axis_y

    def begin(self):
        # Set the current camera offset so you can draw your scene.

        # Translate using the offset.
        view_matrix = self._window.view.translate((-self.offset_x * self._zoom, -self.offset_y * self._zoom, 0))
        # Scale by zoom level.
        view_matrix = view_matrix.scale((self._zoom, self._zoom, 1))

        self._window.view = view_matrix

    def end(self):
        # Since this is a matrix, you will need to reverse the translate after rendering otherwise
        # it will multiply the current offset every draw update pushing it further and further away.

        # Reverse scale, since that was the last transform.
        view_matrix = self._window.view.scale((1 / self._zoom, 1 / self._zoom, 1))
        # Reverse translate.
        view_matrix = view_matrix.translate((self.offset_x * self._zoom, self.offset_y * self._zoom, 0))

        self._window.view = view_matrix

    def __enter__(self):
        self.begin()

    def __exit__(self, exception_type, exception_value, traceback):
        self.end()


class TargetCamera(Camera):
    def __init__(self, window: pyglet.window.Window, target: CoordinateObject, scroll_speed=1, min_zoom=1, max_zoom=4):
        super().__init__(window, scroll_speed, min_zoom, max_zoom)
        self.target = target

    def begin(self):
        x = self.target.x - self._window.width // 2 / self._zoom

        min_y = self.offset_y
        target_y = self.target.y - self._window.height // 2 / self._zoom
        y = max(min_y, target_y)

        view_matrix = self._window.view.translate((-x * self._zoom, -y * self._zoom, 0))
        view_matrix = view_matrix.scale((self._zoom, self._zoom, 1))
        self._window.view = view_matrix

    def end(self):
        x = self.target.x - self._window.width // 2 / self._zoom

        min_y = self.offset_y
        target_y = self.target.y - self._window.height // 2 / self._zoom
        y = max(min_y, target_y)

        view_matrix = self._window.view.scale((1 / self._zoom, 1 / self._zoom, 1))
        view_matrix = view_matrix.translate((x * self._zoom, y * self._zoom, 0))
        self._window.view = view_matrix

    def get_camera_delta(self):
        dx = self._window.width // 2 - self.target.x

        min_y = self.offset_y
        target_y = self._window.height // 2 - self.target.y
        dy = min_y
        if self.target.y >= self._window.height // 2:
            dy += target_y
        else:
            dy += target_y - target_y/self.zoom

        return dx, dy

    def normalize_mouse_pos(self, x, y) -> tuple[float, float]:
        world_x = (x - self._window.width / 2) / self._zoom + self.target.x
        world_y = (y - self._window.height / 2) / self._zoom + self.target.y

        min_y = self.offset_y
        target_y = self.target.y - self._window.height // 2 / self.zoom
        world_y = max(min_y, target_y) + (world_y - target_y)

        return world_x, world_y

    def world_to_screen_pos(self, world_x, world_y) -> tuple[float, float]:
        screen_x = (world_x - self.target.x) * self._zoom + self._window.width / 2
        screen_y = (world_y - self.target.y) * self._zoom + self._window.height / 2

        min_y = self.offset_y
        target_y = self.target.y - self._window.height // 2 / self._zoom
        screen_y -= max(min_y, target_y) * self._zoom - target_y * self._zoom

        return screen_x, screen_y


