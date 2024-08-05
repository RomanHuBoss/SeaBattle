from typing import List
from constants import E_PLAYER_TYPES, E_CELL_VALUES, BOARD_SIZE
from CBoardCell import CBoardCell

class CBoard:
    def __init__(self, owner: E_PLAYER_TYPES):
        self._owner: E_PLAYER_TYPES = owner
        self._data: List[E_CELL_VALUES] = []
        self.reset()

    @property
    def owner(self) -> E_PLAYER_TYPES:
        return self._owner

    @property
    def data(self):
        return self._data

    def reset(self):
        # намеренно (чтоб попрактиковаться) организую одномерный, а не двухмерный массив
        self._data = [CBoardCell() for i in range(BOARD_SIZE * BOARD_SIZE)]

    def get_cell(self, row_index: int, column_index: int) -> CBoardCell:
        return self._data[row_index * BOARD_SIZE + column_index]

    def set_cell_value(self, row_index: int, column_index: int, value: E_PLAYER_TYPES):
        self._data[row_index * BOARD_SIZE + column_index].value = value

    def __str__(self):
        result = '  | ' + ' | '.join(list(map(str, range(1, BOARD_SIZE + 1)))) + ' | \n'
        for row_index in range(0, BOARD_SIZE * BOARD_SIZE, BOARD_SIZE):
            result += f'{int(row_index / BOARD_SIZE) + 1}'
            for column_index in range(row_index, row_index + BOARD_SIZE):
                cell = self.data[column_index]

                # запретим пользователю подглядывать за кораблями ИИ
                cell_value = E_CELL_VALUES.WATER.value if self.owner == E_PLAYER_TYPES.AI and cell == E_CELL_VALUES.SHIP else str(cell)

                result += ' | ' + cell_value
            result += ' | \n'
        return result


if __name__ == "__main__":
    board = CBoard(E_PLAYER_TYPES.AI)
    board.set_cell_value(0, 1, E_CELL_VALUES.BURNING)
    print(board)