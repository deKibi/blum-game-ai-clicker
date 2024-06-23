class ScreenResolution(object):
    def __init__(self, width: int, height: int):
        self._width = width
        self._height = height

    def get_width(self) -> int:
        return self._width

    def get_height(self) -> int:
        return self._height
