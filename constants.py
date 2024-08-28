from enum import Enum

# режим "подсказки" (отображения непораженных кораблей на поле ИИ)
SHOW_AI_SHIPS = False

# размер поля
FIELD_SIZE: int = 6


class EGameStatus(Enum):
    """
    перечисление состояний игры
    """
    NONACTIVE = 'Игра не инициализирована'
    INITIALIZING = 'Игра инициализируется'
    ACTIVE = 'Активная игра'
    FINISHED = 'Игра завершена'


class EShipType(Enum):
    """
    перечисление типов кораблей, их размеров и количеств, доступных к размещению на поле
    """
    TRIPLE = dict(title='Трёхпалубный', size=3, initial_quantity=1)
    DOUBLE = dict(title='Двухпалубный', size=2, initial_quantity=2)
    SINGLE = dict(title='Однопалубный', size=1, initial_quantity=3)


class EShipOrientation(Enum):
    """
    типы ориентации корабля
    """
    HORIZONTAL = dict(title='Горизонтально', numeric_code=1)
    VERTICAL = dict(title='Вертикально', numeric_code=2)


class EPlayer(Enum):
    """
    перечисление типов игроков
    """
    HUMAN = 'Человек'
    AI = 'Искусственный интеллект'


class ECellStatus(Enum):
    """
    перечисление типов статусов клеток игрового поля
    """
    EMPTY = {'title': 'Пустая клетка', 'reflection': '0'}
    FILLED = {'title': 'Клетка занята кораблем', 'reflection': '■', 'reflection_hidden': '0'}
    EXPLODED = {'title': 'Подрыв корабля', 'reflection': 'X'}
    MISSED = {'title': 'Промах', 'reflection': 'T'}


if __name__ == '__main__':
    pass
