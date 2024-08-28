from random import randint
from cfield import CField
from constants import EPlayer, EGameStatus, SHOW_AI_SHIPS


class CGame:
    """
    класс игры
    """
    def __init__(self):
        """
        первичная инициализация
        """
        self._status = EGameStatus.NONACTIVE
        self._mover = None
        self._winner = None
        self._status = None
        self._move_index = 0
        self._fields = []

        for player_type in EPlayer:
            self._fields.append(CField(player_type))

    def start(self):
        """
        начало очередной партии
        :return: None
        """
        self._status = EGameStatus.INITIALIZING
        self._mover = None
        self._winner = None
        self._status = None
        self._move_index = 0

        for field in self._fields:
            field.init()

        self._status = EGameStatus.ACTIVE
        self._mover = EPlayer.AI if randint(1, 2) == 1 else EPlayer.HUMAN

        while self._status != EGameStatus.FINISHED:
            self.next_move()

    def next_move(self):
        self._move_index += 1
        if self._move_index % 2 != 0:
            print("============")

        current_round = int(self._move_index / 2) + 1 if self._move_index % 2 != 0 else int(self._move_index / 2)
        postfix = "Ход ИИ" if self._mover == EPlayer.AI else "Ваш ход"
        print(f"Раунд № {current_round} - {postfix}")

        if self._mover == EPlayer.AI:
            self.ai_shot()
            if not self.human_field.has_undestroyed_ships():
                print("К сожалению, ИИ победил")
                self._status = EGameStatus.FINISHED
        else:
            self.print_both_fields()
            self.human_shot()
            if not self.ai_field.has_undestroyed_ships():
                print("Вы победили! Поздравляем!")
                self._status = EGameStatus.FINISHED

        self._mover = EPlayer.AI if self._mover == EPlayer.HUMAN else EPlayer.HUMAN

    @property
    def human_field(self) -> CField:
        """
        возвращает поле игрока-человека
        :return: CField
        """
        return list(filter(lambda field: field.owner == EPlayer.HUMAN, self._fields))[0]

    @property
    def ai_field(self) -> CField:
        """
        возвращает поле ИИ
        :return: CField
        """
        return list(filter(lambda field: field.owner == EPlayer.AI, self._fields))[0]

    def ai_shot(self):
        """
        выстрел ИИ
        :return: None
        """
        cell = self.human_field.non_shelled_cells[randint(0, len(self.human_field.non_shelled_cells) - 1)]
        self.human_field.shoot_cell(cell)

    def human_shot(self):
        """
        выстрел человека
        :return: None
        """
        while True:
            try:
                x_str, y_str = input(
                    f'Введите X- и Y-координаты обстреливаемой клетки в виде пары целых чисел через пробел: ').split()
                x = int(x_str)
                y = int(y_str)

                if not CField.check_cell_coords((x, y)):
                    raise ValueError()
            except ValueError:
                print("ОШИБКА! Некорректные координаты обстреливаемой клетки")
                continue

            try:
                self.ai_field.shoot_cell((x, y))
            except Exception as e:
                print(e)
                continue

            break

    def print_both_fields(self):
        human_field_strings = self._fields[0].get_field_strings()
        ai_field_strings = self._fields[1].get_field_strings(SHOW_AI_SHIPS)
        common_strings = []

        for i in range(0, len(human_field_strings)):
            common_strings.append(human_field_strings[i] + (' ' * 8) + ai_field_strings[i])

        print('\n'.join(common_strings))


if __name__ == '__main__':
    pass
