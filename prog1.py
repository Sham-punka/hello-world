from collections import Counter
import random

class SizeError(Exception):
    pass

class LenInputError(Exception):
    pass

class NotEmptyError(Exception):
    pass

size = 3    #размер поля
field = [['-'] * (size) for _ in range(size) ]      #игровое поле
symbols = ['X', 'O']        #виды символов



def print_field():      #вывод текущего положения
    title = [str(i) for i in range(size)]
    title.insert(0, " ")
    print(*title)
    map = [['-'] * (size) for _ in range(size) ]
    for i, j in enumerate(field):

        print(f'{i} {" ".join(j)}')


def chek_winer(map):        #проверка на победу
    for i in map:
        if Counter(i)['X'] == size or Counter(i)['O'] == size:
            return True
    for i in range(size):
        line = []
        for j in range(size):
            line.append(map[j][i])
        if Counter(line)['X'] == size or Counter(line)['O'] == size:
            return True
    for j in range(size):
        line = [map[j][j] for j in range(size)]
        if Counter(line)['X'] == size or Counter(line)['O'] == size:
            return True
    for j in range(size):
        line = [map[size - j -1][j] for j in range(size)]
        if Counter(line)['X'] == size or Counter(line)['O'] == size:
            return True


def chek_draw(map):         #проверка на ничью
    flag = []
    for i in map:
        flag.append(Counter(i)['X'] > 0 and Counter(i)['O'] > 0)
    for i in range(size):
        line = []
        for j in range(size):
            line.append(map[j][i])
        flag.append(Counter(line)['X'] > 0 and Counter(line)['O'] > 0)

    line = [map[j][j] for j in range(size)]
    flag.append(Counter(line)['X'] > 0 and Counter(line)['O'] > 0)

    line = [map[size - j -1][j] for j in range(size)]
    flag.append(Counter(line)['X'] > 0 and Counter(line)['O'] > 0)
    #print(flag)
    #print(flag.count(False))
    return all(flag)


def move(symbol):         #ход человека
    new_field = field
    while True:
        point = input(f'Введите через пробел координаты, куда хотите разместить {symbol}:\t').split()
        try:
            if len(point) != 2:
                raise LenInputError
            point[0]= int(point[0])
            point[1] = int(point[1])
            if point[0] > 3 or point[1] > 3:
                raise SizeError
            if new_field[point[0]][point[1]] != '-':

                raise NotEmptyError
            break
        except(SizeError):
            print("Введите координаты не превышающие 3")
        except(LenInputError):
            print('Введите два целых числа!')
        except(NotEmptyError):
            print('Здесь уже занято! Выберите другое место')
        except:
            print("Введено некоректное значение. Введите два целых числа!")
    new_field[point[0]][point[1]] = symbol
    return new_field


def computer_move(symbol):      #ход компьютера
    new_field = field
    empty_points = []
    for i in range(3):
        for j in range(3):
            if new_field[i][j] == '-':
                empty_points.append((i, j))
    choice_point = random.choice(empty_points)
    new_field[choice_point[0]][choice_point[1]] = symbol
    return new_field


def play_with_human():
    global field
    for _ in range(4):  # Вывод  пока победы точно не может быть

        field = move(symbols[0])
        print_field()
        symbols.reverse()

    for i in range(5):
        field = move(symbols[0])
        print_field()

        if chek_winer(field):
            print(f'Игра окончена! Победили {symbols[0]}')
            break
        if i == 4:
            if chek_draw(field):
                print(f'Игра окончена! НИЧЬЯ')
        symbols.reverse()


def play_with_computer(first):
    global field
    if first == 1:      #начинает человек
       for _ in range(2):
           field = move(symbols[0])
           print_field()
           symbols.reverse()
           print('Ход компьютера')
           field = computer_move(symbols[0])
           print_field()
           symbols.reverse()

       for i in range(3):
           field = move(symbols[0])
           print_field()

           if chek_winer(field):
               print(f'Игра окончена! Победили {symbols[0]}')
               break
           if i == 2:
               if chek_draw(field):
                   print(f'Игра окончена! НИЧЬЯ')
                   break
           symbols.reverse()

           print('ход компьютера')

           field = computer_move(symbols[0])
           print_field()

           if chek_winer(field):
               print(f'Игра окончена! Победили {symbols[0]}')
               break
           if i == 2:
               if chek_draw(field):
                   print(f'Игра окончена! НИЧЬЯ')
                   break
           symbols.reverse()
    else:       #начинает компьютер
        for _ in range(2):
            print('Ход компьютера')
            field = computer_move(symbols[0])
            print_field()
            symbols.reverse()

            field = move(symbols[0])
            print_field()
            symbols.reverse()

        for i in range(3):
            print('Ход компьютера')
            field = computer_move(symbols[0])
            print_field()
            if chek_winer(field):
                print(f'Игра окончена! Победили {symbols[0]}')
                break
            if i == 2:
                if chek_draw(field):
                    print(f'Игра окончена! НИЧЬЯ')
                    break
            symbols.reverse()

            field = move(symbols[0])
            print_field()
            if chek_winer(field):
                print(f'Игра окончена! Победили {symbols[0]}')
                break
            if i == 2:
                if chek_draw(field):
                    print(f'Игра окончена! НИЧЬЯ')
                    break
            symbols.reverse()


type_game = input(""""Выбирите режим игры:
С человеком: Введите ч
С компьютером: Введите к
""")

while type_game not in 'чк':
    type_game = input(""""С человеком: Введите ч
С компьютером: Введите к
""")

if type_game == 'ч':
    print_field()
    play_with_human()
elif type_game == 'к':
    print_field()
    first = random.choice([1, 2])     #1- начинает человек, 2- начинает компьютер
    play_with_computer(first)
else:
    print('''С человеком: Введите ч
С компьютером: Введите к''')










