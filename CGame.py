from typing import List
from constants import E_PLAYER_TYPES, E_GAME_STATUSES, INITIAL_SHIP_SET
from CBoard import CBoard
from CShip import CShip, CThreeDeckShip, CTwoDeckShip, CSingleDeckShip

class CGame:

    def __init__(self):
        self._status: E_GAME_STATUSES = None
        self._boards: List[CBoard] = []
        self._boards.append(CBoard(E_PLAYER_TYPES.HUMAN))
        self._boards.append(CBoard(E_PLAYER_TYPES.AI))

    def start(self):
        if self._status is not None and self._status != E_GAME_STATUSES.FINISHED:
            raise Exception('Ошибочная инициализация игры')

        self._status = E_GAME_STATUSES.INITIALIZING

        self.generate_ai_board()

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status: E_GAME_STATUSES) -> None:
        if (
                (status == self._status)
                or (status == E_GAME_STATUSES.INITIALIZING and not self._status in [None, E_GAME_STATUSES.FINISHED])
                or (status == E_GAME_STATUSES.PLAYING and self._status != E_GAME_STATUSES.INITIALIZING)
                or (status == E_GAME_STATUSES.FINISHED and self._status != E_GAME_STATUSES.PLAYING)
        ):
            exception_text = f'Игре не может быть назначен статус "{status.value}"'

            if not self._status is None:
                exception_text += f', поскольку текущий статус "{self._status.value}"'
            else:
                exception_text += f', поскольку игра не инициализирована'

            raise Exception(exception_text)

        self._status = status

    def generate_ai_board(self):
        for ship_type, quantity in INITIAL_SHIP_SET.items():
            print(eval(ship_type), quantity)


    def step(self):
        pass
