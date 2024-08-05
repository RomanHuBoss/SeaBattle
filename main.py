from CGame import CGame
from constants import E_GAME_STATUSES

game = CGame()

while True:
    game.start()
    game.status = E_GAME_STATUSES(E_GAME_STATUSES.PLAYING)
    if input('Хотите сыграть еще раз (y/n)? ').lower() != 'y':
        break