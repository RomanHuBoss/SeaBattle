from enum import Enum

# размер доски (может быть изменен)
BOARD_SIZE = 6

# типы игроков
E_PLAYER_TYPES = Enum('E_PLAYER_TYPE', ['HUMAN', 'AI'])

# статусы игры
E_GAME_STATUSES = Enum('E_GAME_STATUSES', {
    'INITIALIZING': 'инициализация игры',  # игра инициализируется
    'PLAYING': 'активная игра',  # активный процесс игры
    'FINISHED': 'игра завершена'  # игра завершена
})

# возможные значения клеток игрового поля
E_CELL_VALUES = Enum('E_CELL_VALUES', {
    'WATER': 'О',  # водичка
    'SHIP': '■',  # занята кораблем
    'BURNING': 'X',  # подбит корабль (горит)
    'MISSED': 'T'  # обстреляна, но там не было корабля
})

# исходный набор кораблей у каждого из игроков
INITIAL_SHIP_SET = {'CThreeDeckShip': 1, 'CTwoDeckShip': 2, 'CSingleDeckShip': 3}
