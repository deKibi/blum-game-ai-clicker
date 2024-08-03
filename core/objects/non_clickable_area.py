# core/objects/non_clickable_area.py

class NonClickableArea(object):
    def __init__(self, padding_left: int, padding_right: int, padding_top: int, padding_bottom: int):
        self._padding_left: int = padding_left
        self._padding_right: int = padding_right
        self._padding_top: int = padding_top
        self._padding_bottom: int = padding_bottom

    def get_padding_left(self) -> int:
        return self._padding_left

    def get_padding_right(self) -> int:
        return self._padding_right

    def get_padding_top(self) -> int:
        return self._padding_top

    def get_padding_bottom(self) -> int:
        return self._padding_bottom
