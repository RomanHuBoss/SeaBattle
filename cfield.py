from random import randint
from constants import FIELD_SIZE, EShipType, EShipOrientation, EPlayer, ECellStatus
from cship import CShip


class CField:
    """
    класс игрового поля
    """

    def __init__(self, owner: EPlayer):
        """
        :param owner: владелец поля (см. constants.py)
        """
        self._owner = owner
        self._ships = []
        self._shelled_cells = []
        self._all_cells = [(x, y) for x in range(1, FIELD_SIZE + 1) for y in range(1, FIELD_SIZE + 1)]

    def clear(self):
        """
        очистка игрового поля
        :return: None
        """
        for _ in self._ships:
            del _

        self._ships = []
        self._shelled_cells = []

    def init(self):
        """
        инициализация игрового поля
        :return: None
        """
        self.clear()
        if self.owner == EPlayer.AI:
            self.arrange_ai_ships()
        else:
            self.arrange_human_ships()

    def arrange_ai_ships(self) -> int:
        """
        расстановка кораблей игрока-ИИ
        :return: None
        """
        iterations = 0
        for ship_type in EShipType:
            ship_type_data = ship_type.value
            for i in range(1, ship_type_data['initial_quantity'] + 1):
                while True:
                    iterations += 1
                    x = randint(1, FIELD_SIZE)
                    y = randint(1, FIELD_SIZE)
                    orientation = EShipOrientation.HORIZONTAL if randint(1,
                                                                         2) == EShipOrientation.HORIZONTAL.value[
                                                                     "numeric_code"] else EShipOrientation.VERTICAL
                    try:
                        ship = CShip(x, y, ship_type, orientation)
                        if not self.check_ship_add_ability(ship):
                            raise ValueError()
                        self.add_ship(ship)
                    except ValueError:
                        continue

                    break

        return iterations

    def arrange_human_ships(self):
        """
        расстановка кораблей игрока-человека
        :return: None
        """
        for ship_type in EShipType:
            ship_type_data = ship_type.value
            for i in range(1, ship_type_data['initial_quantity'] + 1):
                orientation = None

                while True:
                    print(self)
                    try:
                        x_str, y_str = input(
                            f'Введите X- и Y-координаты точки привязки корабля типа "{ship_type_data["title"]}" '
                            f'в виде пары целых чисел через пробел: ').split()
                        x = int(x_str)
                        y = int(y_str)

                        if not CField.check_cell_coords((x, y)):
                            raise ValueError()
                    except ValueError:
                        print("ОШИБКА! Некорректные координаты точки привязки корабля")
                        continue

                    if self.get_cell_status((x, y)) in [ECellStatus.FILLED, ECellStatus.EXPLODED]:
                        print("ОШИБКА! Координаты точки привязки корабля уже заняты")
                        continue

                    if self.has_cell_filled_neighbours((x, y)):
                        print("ОШИБКА! Корабль не может быть размещен в непосредственной близости с занятыми клетками")
                        continue

                    if ship_type_data["size"] > 1:
                        try:
                            orientation_code = int(input(
                                f'Для размещения корабля {EShipOrientation.HORIZONTAL.value["title"].lower()} '
                                f'введите {EShipOrientation.HORIZONTAL.value["numeric_code"]}, для размещения '
                                f'{EShipOrientation.VERTICAL.value["title"].lower()} - введите '
                                f'{EShipOrientation.VERTICAL.value["numeric_code"]}: '))
                            if orientation_code == EShipOrientation.HORIZONTAL.value["numeric_code"]:
                                orientation = EShipOrientation.HORIZONTAL
                            elif orientation_code == EShipOrientation.VERTICAL.value["numeric_code"]:
                                orientation = EShipOrientation.VERTICAL
                            else:
                                raise ValueError()
                        except ValueError:
                            print("ОШИБКА! Некорректный тип размещения корабля")
                            continue

                    try:
                        ship = CShip(x, y, ship_type, orientation)
                        if not self.check_ship_add_ability(ship):
                            raise Exception(
                                "ОШИБКА! Корабль не может быть размещен в "
                                "непосредственной близости с занятыми клетками")
                    except Exception as e:
                        print(e)
                        continue

                    self.add_ship(ship)

                    break

    @staticmethod
    def check_cell_coords(cell: (int, int)) -> bool:
        """
        проверка на допустимость координат клетки
        :param cell: координаты клетки (x, y)
        :return: bool
        """
        cell_x, cell_y = cell[0], cell[1]
        return (1 <= cell_x <= FIELD_SIZE) and (1 <= cell_y <= FIELD_SIZE)

    def has_cell_filled_neighbours(self, cell: (int, int)) -> bool:
        """
        проверка наличия занятых клеток, соседних по отношению к заданной
        :param cell: координаты клетки (x, y)
        :return: bool
        """
        if not CField.check_cell_coords(cell):
            raise Exception("ОШИБКА! Координаты клетки выходят за рамки игрового поля")

        cell_x, cell_y = cell[0], cell[1]

        neighbours = list(filter(CField.check_cell_coords,
                                 [(cell_x, cell_y - 1), (cell_x + 1, cell_y), (cell_x, cell_y + 1),
                                  (cell_x - 1, cell_y)]
                                 ))

        filled_neighbours = list(
            filter(lambda neighbour_cell:
                   self.get_cell_status(neighbour_cell) in [ECellStatus.FILLED, ECellStatus.EXPLODED],
                   neighbours))

        return len(filled_neighbours) > 0

    def check_ship_add_ability(self, ship: CShip) -> bool:
        """
        проверяем, может ли корабль быть размещен на игровом поле
        :param ship:
        :return: bool
        """
        return len(list(filter(lambda cell: self.has_cell_filled_neighbours(cell), ship.occupied_cells))) == 0

    @property
    def ships(self):
        """
        возвращает список кораблей на поле
        :return: list[CShip]
        """
        return self._ships.copy()

    @property
    def owner(self) -> EPlayer:
        """
        возвращает владельца поля (см. constants.py)
        :return: EPlayer
        """
        return self._owner

    @property
    def shelled_cells(self):
        """
        возвращает список обстрелянных клеток
        :return: list[(int, int)]
        """
        return self._shelled_cells.copy()

    @property
    def non_shelled_cells(self):
        """
        возвращает список необстрелянных клеток
        :return: list[(int, int)]
        """
        return [cell for cell in self._all_cells if cell not in self._shelled_cells]

    def add_shelled_cell(self, cell: (int, int)):
        """
        добавляет клетку поля в список обстрелянных
        :param cell: клетка
        :return: None
        """
        self._shelled_cells.append(cell)

    def add_ship(self, ship: CShip):
        """
        добавляет корабль на поле
        :param ship: корабль
        :return: None
        """
        self._ships.append(ship)

    @property
    def occupied_cells(self):
        """
        возвращает список клеток, занятых кораблями
        :return: list[(int, int)]
        """
        occupied_cells = []
        for ship in self.ships:
            occupied_cells += ship.occupied_cells
        return occupied_cells

    @property
    def exploded_cells(self):
        """
        возвращает список клеток, в которых горят корабли
        :return: list[(int, int)]
        """
        exploded_cells = []
        for ship in self.ships:
            exploded_cells += ship.exploded_cells
        return exploded_cells

    def get_cell_status(self, cell: (int, int)) -> ECellStatus:
        """
        возвращает статус клетки
        :return: ECellStatus
        """
        if cell not in self._shelled_cells:
            status = ECellStatus.EMPTY if cell not in self.occupied_cells else ECellStatus.FILLED
        else:
            status = ECellStatus.EXPLODED if cell not in self.exploded_cells else ECellStatus.MISSED

        return status

    def get_field_strings(self, show_ai_ships=False):
        """
        возвращает список строк поля
        :return: list[str]
        """
        strings = []
        for y in range(0, FIELD_SIZE + 1):
            if y == 0:  # первая строка
                tmp = "  | " + ' | '.join(str(x) for x in range(1, 7)) + " |"
                strings.append(tmp)
            else:
                tmp = f"{y} | "
                cell_reflections = []
                for x in range(1, FIELD_SIZE + 1):
                    cell_status = self.get_cell_status((x, y))
                    if self.owner == EPlayer.AI and cell_status == ECellStatus.FILLED and not show_ai_ships:
                        cell_status = ECellStatus.EMPTY
                    cell_reflections.append(cell_status.value["reflection"])
                tmp = tmp + ' | '.join(cell_reflections) + ' |'
                strings.append(tmp)

        first_string = "Игровое поле ИИ" if self.owner == EPlayer.AI else "Ваше игровое поле"
        first_string = first_string.center(len(strings[0]))

        strings = [first_string] + strings

        return strings

    def shoot_cell(self, cell: (int, int)):
        """
        обстрел клетки
        :param cell: (int, int)
        :return: None
        """
        if cell in self._shelled_cells:
            raise Exception("ОШИБКА! Нельзя многократно обстреливать одну и ту же клетку")

        self.add_shelled_cell(cell)

        if cell in self.occupied_cells:  # попали в корабль
            for ship in self._ships:
                if ship.is_cell_occupant(cell):
                    ship.add_exploded_cell(cell)
                    if ship.is_destroyed():
                        if self._owner == EPlayer.HUMAN:
                            print(f"ИИ обстрелял клетку с координатами {cell[0], cell[1]} "
                                  f"и уничтожил ваш {ship.title.lower()} корабль")
                        elif self._owner == EPlayer.AI:
                            print(f"Вы уничтожили {ship.title.lower()} корабль")
                    else:
                        if self._owner == EPlayer.HUMAN:
                            print(f"ИИ обстрелял клетку с координатами {cell[0], cell[1]} "
                                  f"и подбил ваш {ship.title.lower()} корабль")
                        elif self._owner == EPlayer.AI:
                            print(f"Вы подбили {ship.title.lower()} корабль")
                    break
        else:
            phrase = f"ИИ обстрелял клетку с координатами {cell[0], cell[1]} и промахнулся" \
                if self._owner == EPlayer.HUMAN \
                else "Вы промахнулись"
            print(phrase)

    def has_undestroyed_ships(self) -> bool:
        """
        проверяет, есть ли еще неуничтоженные корабли на поле
        :return: bool
        """
        return len(list(filter(lambda ship: not ship.is_destroyed(), self._ships))) > 0

    def __str__(self):
        """
        преобразование поля к строковому виду
        :return: str
        """
        return "\n".join(self.get_field_strings())


if __name__ == '__main__':
    # field = CField(EPlayer.HUMAN)
    # print(field.non_shelled_cells)
    pass
