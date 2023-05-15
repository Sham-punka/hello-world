from random import *


class FieldException(Exception):
    pass


class NotEmptyException(FieldException):
    def __str__(self):
        return "В эту клетку уже стреляли"


class OutException(FieldException):
    def __str__(self):
        return "Эта точка за пределами поля"


class ShipException(Exception):
    pass


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

class Ship:
    def __init__(self, start, long, course):
        self.course = course
        self.start = start
        self.long = long
        self.hp = long

    def points(self):
        ship_points = []
        for i in range(self.long):
            x = self.start.x
            y = self.start.y

            if self.course == 0:
                x += i

            elif self.course == 1:
                y += i

            ship_points.append(Point(x, y))

        return ship_points

    def shoot(self, pt):
        return pt in self.points

class Field:
    def __init__(self, open=False, size = 6):
        self.open = open
        self.size = size
        self.dships = 0
        self.map = [["0"]*self.size for _ in range(self.size)]
        self.occupied = []
        self.ships = []

    def __str__(self):
        st = ""
        st += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.map):
            st += f"\n{i+1} | " + " | ".join(row) + " |"

        if self.open:
            st = st.replace("■", "О")
        return st

    def out(self, d):
        return not((0 <= d.x < self.size) and (0 <= d.y < self.size))

    def contour(self, ship, np=False):
        near = [(0, 0), (0, 1), (0, -1), (1, 0), (1, 1), (1, -1), (-1, 0), (-1, 1), (-1, -1)]
        for i in ship.points():
            for jx, jy in near:
                pt = Point(i.x + jx, i.y + jy)
                if not(self.out(pt)) and pt not in self.occupied:
                    if np:
                        self.map[pt.x][pt.y] = "."
                    self.occupied.append(pt)

    def add_ship(self, ship):

        for i in ship.points():
            if self.out(i) or i in self.occupied:
                raise ShipException()
        for i in ship.points():
            self.map[i.x][i.y] = "■"
            self.occupied.append(i)

        self.ships.append(ship)
        self.contour(ship)

    def shot(self, i):
        if i in self.occupied:
            raise NotEmptyException()

        if self.out(i):
            raise OutException()

        self.occupied.append(i)

        for ship in self.ships:
            if i in ship.points():
                ship.hp -= 1
                self.map[i.x][i.y] = "X"
                if ship.hp != 0:
                    print("Ранен!")
                    return True
                else:
                    self.dships += 1
                    self.contour(ship, np=True)
                    print("Убил!")
                    return False

        self.map[i.x][i.y] = "Т"
        print("Мимо!")
        return False

    def begining(self):
        self.occupied = []

class Player:
    def __init__(self, field, enemy):
        self.field = field
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except FieldException as er:
                print(er)

class AI(Player):
    def ask(self):
        pt = Point(randint(0,5), randint(0, 5))
        print(f"Ход компьютера: {pt.x+1} {pt.y+1}")
        return pt


class User(Player):
    def ask(self):
        while True:
            cords = input("Введите 2 координаты чекрез пробел: ").split()

            if len(cords) != 2:
                print("Введите 2 координаты! ")
                continue

            x, y = cords

            if not (x.isdigit()) or not (y.isdigit()):
                print("Введите числа! ")
                continue

            x, y = int(x), int(y)

            return Point(x - 1, y - 1)


class Game:
    def __init__(self, size = 6):
        self.size = size
        player = self.random_board()
        computer = self.random_board()
        computer.open = True

        self.ai = AI(computer, player)
        self.us = User(player, computer)

    def random_board(self):
        field = None
        while field is None:
            field = self.random_place()
        return field

    def random_place(self):
        lens = [3, 2, 2, 1, 1, 1, 1]
        field = Field(size=self.size)
        attempts = 0
        for l in lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Point(randint(0, self.size), randint(0, self.size)), l, randint(0, 1))
                try:
                    field.add_ship(ship)
                    break
                except ShipException:
                    pass
        field.begining()
        return field

    def play(self):
        num = 0
        while True:
            print()
            print("Доска игрока:")
            print(self.us.field)
            print()
            print("Доска компьютера:")
            print(self.ai.field)
            if num % 2 == 0:
                print()
                print("Ходит пользователь!")
                repeat = self.us.move()
            else:
                print()
                print("Ходит компьютер!")
                repeat = self.ai.move()
            if repeat:
                num += 1

            if self.ai.field.dships == 7:
                print()
                print("Игрок выиграл!")
                break

            if self.us.field.dships== 7:
                print()
                print("Компьютер выиграл!")
                break
            num -= 1

    def start(self):
        self.play()

g = Game()
g.start()






