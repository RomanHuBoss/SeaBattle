from constants import E_CELL_VALUES


class CBoardCell:
    def __init__(self):
        self._value: E_CELL_VALUES = E_CELL_VALUES.WATER

    @property
    def value(self) -> E_CELL_VALUES:
        return self._value

    @value.setter
    def value(self, value: E_CELL_VALUES):
        self._value = value

    def __str__(self):        
        return self._value.value
