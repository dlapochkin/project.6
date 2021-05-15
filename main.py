import string
from random import *


def main():
    board, stats = cleaner(preparation())
    table(board, stats)
    turn(board, stats)


def preparation():
    nums = '123456789'
    pattern = ''
    for x in range(9):
        pattern += nums[x:] + nums[:x]
    clear = dict(zip([(x, y) for x in 'abcdefghi' for y in range(1, 10)], [x for x in pattern]))
    return shuffler(clear)


def shuffler(board):
    for shuff in range(32):
        i = randint(0, 2)
        if i == 0:
            board = transposition(board)
        elif i == 1:
            board = row_shuffle(board)
        else:
            board = column_shuffle(board)
    return board


def transposition(board):
    transposed = {}
    for (x, y) in board:
        transposed[(x, y)] = board[(chr(y+96), ord(x)-96)]
    return transposed


def row_shuffle(board):
    if i == 0:
        alphabet = list('abc')
    elif i == 1:
        alphabet = list('def')
    else:
        alphabet = list('ghi')
    x = choice(alphabet)
    del alphabet[alphabet.index(x)]
    y = choice(alphabet)
    for z in range(1, 10):
        temp = board[(x, z)]
        board[(x, z)] = board[(y, z)]
        board[(y, z)] = temp
    return board


def column_shuffle(board):
    i = randint(0, 2)
    if i == 0:
        alphabet = list('123')
    elif i == 1:
        alphabet = list('456')
    else:
        alphabet = list('789')
    x = int(choice(alphabet))
    del alphabet[alphabet.index(str(x))]
    y = int(choice(alphabet))
    for z in 'abcdefghi':
        temp = board[(z, x)]
        board[(z, x)] = board[(z, y)]
        board[(z, y)] = temp
    return board


def cleaner(board):
    beginning = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0, '8': 0, '9': 0, 'turn': 0}
    i = 81 - int(input('Введите число подсказок (рекомендуется использовать числа в диапазоне от 30 до 35): '))
    while i > 0:
        a, b = choice(list('abcdefghi')), randint(1, 9)
        if board[(a, b)] == '0':
            continue
        beginning[board[(a, b)]] += 1
        board[(a, b)] = '0'
        i -= 1
    return board, beginning


def table(board, stats):
    tree = board.copy()
    for key in tree:
        if tree[key] == '0':
            tree[key] = ' '
    simple = list(tree.values())
    print('{:-^37s}'.format(''), '{: ^9s}'.format(''), '{:-^9s}'.format('Числа'))
    for x in range(9):
        print('|{:^3s}|{:^3s}|{:^3s}|{:^3s}|{:^3s}|{:^3s}|{:^3s}|{:^3s}|{:^3s}|'.format(*simple[x*9:x*9+9]),
              string.ascii_lowercase[x], '{:^7s}'.format(''), '|{:^7s}|'.format(str(x+1) + ': ' + str(stats[str(x+1)])))
        print('{:-^37s}'.format(''), '{:^9s}'.format(''), '{:-^9s}'.format(''))
    print(' {:^4d}{:^4d}{:^4d}{:^4d}{:^4d}{:^4d}{:^4d}{:^4d}{:^4d}'.format(*[x for x in range(1, 10)]),
          '{:^9s}'.format(''), '{:^9s}'.format('Ход: ' + str(stats['turn'])), '\n')


def turn(board, stats):
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


main()