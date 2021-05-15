import string
from random import *


def main():
    board, stats = cleaner(preparation())
    table(board, stats)


def preparation():
    nums = '123456789'
    pattern = ''
    for x in range(9):
        pattern += nums[x:] + nums[:x]
    clear = dict(zip([(x, y) for x in 'abcdefghi' for y in range(1, 10)], [x for x in pattern]))
    return clear


def cleaner(board):
    beginning = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0, '8': 0, '9': 0, 'turn': 0}
    i = 81 - int(input('Введите число подсказок (рекомендуется использовать числа в диапазоне от 30 до 35): '))
    while i > 0:
        a, b = choice(list('abcdefghi')), randint(1, 9)
        if board[(a, b)] == 0:
            continue
        beginning[board[(a, b)]] += 1
        board[(a, b)] = 0
        i -= 1
    return board, beginning


def table(board, stats):
    for key in board:
        if board[key] == 0:
            board[key] = ' '
    simple = list(board.values())
    print('{:-^37s}'.format(''), '{: ^9s}'.format(''), '{:-^9s}'.format('Числа'))
    for x in range(9):
        print('|{:^3s}|{:^3s}|{:^3s}|{:^3s}|{:^3s}|{:^3s}|{:^3s}|{:^3s}|{:^3s}|'.format(*simple[x*9:x*9+9]),
              string.ascii_lowercase[x], '{:^7s}'.format(''), '|{:^7s}|'.format(str(x+1) + ': ' + str(stats[str(x+1)])))
        print('{:-^37s}'.format(''), '{:^9s}'.format(''), '{:-^9s}'.format(''))
    print(' {:^4d}{:^4d}{:^4d}{:^4d}{:^4d}{:^4d}{:^4d}{:^4d}{:^4d}'.format(*[x for x in range(1, 10)]),
          '{:^9s}'.format(''), '{:^9s}'.format('Ход:' + str(stats['turn'])))


def receiver():
    return None


main()