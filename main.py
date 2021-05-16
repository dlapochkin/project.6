import string
from random import *


def main():
    """
    Main function
    :return: None
    """
    board, stats = cleaner(preparation())
    table(board, stats)
    turn(board, stats)


def preparation():
    """
    Creates board pattern and dictionary, containing board values
    :return: Shuffled board
    """
    pattern = '123456789' \
              '456789123' \
              '789123456' \
              '234567891' \
              '567891234' \
              '891234567' \
              '345678912' \
              '678912345' \
              '912345678'
    clear = dict(zip([(x, y) for x in 'abcdefghi' for y in range(1, 10)], [x for x in pattern]))
    return shuffler(clear)


def shuffler(board):
    """
    Shuffles board values using random rows and columns swaps and transposition of the board
    :param board: dictionary, containing board values
    :return: board with shuffled values
    """
    shuffling = {0: rows_moving, 1: columns_moving, 2: transposition}
    for shuff in range(256):
        board = shuffling[randint(0, 2)](board)
    return board


def transposition(board):
    """
    Swaps rows and columns of the board
    :param board: dictionary, containing board values
    :return: transposed board
    """
    transposed = {}
    for (x, y) in board:
        transposed[(x, y)] = board[(chr(y + 96), ord(x) - 96)]
    return transposed


def rows_moving(board):
    """
    Swaps two random rows in one sector
    :param board: dictionary, containing board values
    :return: board with moved rows
    """
    sectors = {0: 'abc', 1: 'def', 2: 'ghi'}
    rows = sectors[randint(0, 2)]
    x = choice(rows)
    rows = rows[:rows.find(x)] + rows[rows.find(x) + 1:]
    y = choice(rows)
    for z in '123456789':
        temp = board[(x, int(z))]
        board[(x, int(z))] = board[(y, int(z))]
        board[(y, int(z))] = temp
    return board


def columns_moving(board):
    """
    Swaps two random columns in one sector
    :param board: dictionary, containing board values
    :return: board with moved columns
    """
    sectors = {0: '123', 1: '456', 2: '789'}
    columns = sectors[randint(0, 2)]
    x = choice(columns)
    columns = columns[:columns.find(x)] + columns[columns.find(x) + 1:]
    y = choice(columns)
    for z in 'abcdefghi':
        temp = board[(z, int(x))]
        board[(z, int(x))] = board[(z, int(y))]
        board[(z, int(y))] = temp
    return board


def cleaner(board):
    """
    Hides random squares, leaves given amount of hints
    :param board: dictionary, containing board values
    :return: prepared board, start statistic
    """
    stats = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0, '8': 0, '9': 0, 'turn': 0}
    i = 81 - int(input('Введите число подсказок (рекомендуется использовать числа в диапазоне от 30 до 35): '))
    while i > 0:
        a, b = choice(list('abcdefghi')), randint(1, 9)
        if board[(a, b)] == '0':
            continue
        stats[board[(a, b)]] += 1
        board[(a, b)] = '0'
        i -= 1
    return board, stats


def table(board, stats):
    """
    Prints game board, statistics
    :param board: dictionary, containing board values
    :param stats: dictionary, containing game statistics
    :return: None
    """
    tree = board.copy()
    for key in tree:
        if tree[key] == '0':
            tree[key] = ' '
    simple = list(tree.values())
    print('+---' * 9 + '+', '{: ^9s}'.format(''), '+{:-^7s}+'.format('Числа'))
    for x in range(9):
        print('|{:^3s}:{:^3s}:{:^3s}|{:^3s}:{:^3s}:{:^3s}|{:^3s}:{:^3s}:{:^3s}|'.format(*simple[x * 9:x * 9 + 9]),
              string.ascii_lowercase[x], '{:^7s}'.format(''),
              '|{:^7s}|'.format(str(x + 1) + ': ' + str(stats[str(x + 1)])))
        if x in [2, 5, 8]:
            print('+---' * 9 + '+', '{:^9s}'.format(''), '+{:-^7s}+'.format(''))
        else:
            print('+...' * 9 + '+', '{:^9s}'.format(''), '+{:-^7s}+'.format(''))
    print(' {:^4d}{:^4d}{:^4d}{:^4d}{:^4d}{:^4d}{:^4d}{:^4d}{:^4d}'.format(*[x for x in range(1, 10)]),
          '{:^9s}'.format(''), '{:^9s}'.format('Ход: ' + str(stats['turn'])), '\n')


def turn(board, stats):
    """
    Recursive function representing a game move
    :param board: dictionary, containing board values
    :param stats: dictionary, containing game statistics
    :return: None
    """
    try:
        move = input().split()
        key = list(move[0])[0], int(list(move[0])[1])
        if len(move) == 1:
            if board[key] != '0':
                stats[board[key]] += 1
                board[key] = '0'
            else:
                print('Клетка уже пуста. Попробуйте еще раз.')
                return turn(board, stats)
        else:
            value = move[1]
            if value not in '123456789':
                print('Ошибка ввода. Попробуйте еще раз.')
                return turn(board, stats)
            if stats[value] == 0 and board[key] != value:
                print('Ошибка. Данное число уже использовано 9 раз.')
                return turn(board, stats)
            if board[key] != '0':
                stats[board[key]] += 1
            board[key] = value
            stats[value] -= 1
        stats['turn'] += 1
        table(board, stats)
        if sum(stats.values()) - stats['turn'] == 0 and checker(board):
            print('Поздравляем. Судоку решено за', stats['turn'], 'ходов.')
            exit()
    except KeyError:
        print('Ошибка ввода. Попробуйте еще раз.')
        return turn(board, stats)
    return turn(board, stats)


def checker(board):
    """
    Check if board filled in correctly (with no repetitions)
    :param board: dictionary, containing board values
    :return: True or False
    """
    lines = {}
    for x in 'abcdefghi':
        lines[x] = [board[(x, 1)]]
        for y in range(2, 10):
            lines[x].append(board[(x, y)])
    for x in range(1, 10):
        lines[x] = [board[('a', x)]]
        for y in 'bcdefghi':
            lines[x].append(board[(y, x)])
    for line in list(lines.values()):
        for z in range(1, 10):
            if line.count(str(z)) > 1:
                return False
    return True


if __name__ == '__main__':
    main()
