from cgame import CGame

game = CGame()

while True:
    try:
        answer = input("Вы действительно хотите начать играть в \"Морской бой\" (Y/N)? ")
        answer = answer.lower()
        if answer not in ['y', 'n']:
            raise ValueError()
        if answer == 'n':
            print("До скорых встреч!")
            break
    except ValueError:
        print("Некорректный ответ")
        continue

    game.start()
