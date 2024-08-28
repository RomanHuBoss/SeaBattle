from constants import FIELD_SIZE, EShipType, EShipOrientation


class CShip:
    """
    класс корабля
    """

    def __init__(self, anchor_x: int, anchor_y: int, ship_type: EShipType, orientation: EShipOrientation = None):
        """
        :param anchor_x: X-координата точки привязки корабля
        :param anchor_y: Y-координата точки привязки корабля
        :param ship_type: тип корабля (см. constants.py)
        :param orientation: ориентация корабля (см. constants.py)
        """
        self._occupied_cells = []
        self._exploded_cells = []
        self._ship_size, self._ship_title = ship_type.value['size'], ship_type.value['title']

        if orientation is not None and orientation not in EShipOrientation:
            raise ValueError("ОШИБКА! Некорректное значение ориентации корабля")

        if anchor_x < 1 or anchor_x > FIELD_SIZE:
            raise ValueError("ОШИБКА! Некорректное значение X-координаты опорной точки корабля")
        elif anchor_y < 1 or anchor_y > FIELD_SIZE:
            raise ValueError("ОШИБКА! Некорректное значение Y-координаты опорной точки корабля")

        if orientation == EShipOrientation.HORIZONTAL and anchor_x + self._ship_size - 1 > FIELD_SIZE or \
                orientation == EShipOrientation.VERTICAL and anchor_y + self._ship_size - 1 > FIELD_SIZE:
            raise ValueError(
                f"ОШИБКА! Корабль размера {self._ship_size} не может быть установлен "
                f"{orientation.value['title'].lower()}, начиная с клетки ({anchor_x}, {anchor_y})")

        if self._ship_size == 1:
            self._occupied_cells.append((anchor_x, anchor_y))
        elif orientation == EShipOrientation.VERTICAL:
            for y in range(anchor_y, anchor_y + self._ship_size):
                self._occupied_cells.append((anchor_x, y))
        elif orientation == EShipOrientation.HORIZONTAL:
            for x in range(anchor_x, anchor_x + self._ship_size):
                self._occupied_cells.append((x, anchor_y))

    @property
    def occupied_cells(self):
        """
        возвращает список занятых кораблем клеток
        :return: list[(int, int)]
        """
        return self._occupied_cells.copy()

    @property
    def exploded_cells(self):
        """
        возвращает список подбитых клеток, занятых кораблём
        :return: list[(int, int)]
        """
        return self._exploded_cells.copy()

    def add_exploded_cell(self, cell: (int, int)):
        """
        добавлят клетку к списку подбитых
        :param cell:
        :return: None
        """
        if cell not in self._occupied_cells:
            raise Exception("Клетка не принадлежит указанному кораблю и не может добавлена в список взорванных")

        self._exploded_cells.append(cell)

    def is_cell_occupant(self, cell: (int, int)) -> bool:
        """
        занимает ли корабль заданную клетку
        :param cell: (int, int)
        :return: bool
        """
        return cell in self._occupied_cells

    def is_destroyed(self) -> bool:
        """
        проверка уничтоженности корабля
        :return: bool
        """
        return len(list(set(self._occupied_cells) - set(self._exploded_cells))) == 0

    @property
    def title(self) -> str:
        """
        возвращает строковое название корабля
        :return: str
        """
        return self._ship_title


if __name__ == '__main__':
    pass
