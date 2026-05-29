#5.3.2
from math import gcd


# =====================================================
# Клас Rational
# =====================================================

class Rational:

    def __init__(self, *args):

        # Копіювання
        if len(args) == 1 and isinstance(args[0], Rational):
            self.n = args[0].n
            self.d = args[0].d

        # Рядок "n/d"
        elif len(args) == 1 and isinstance(args[0], str):

            if '/' in args[0]:
                n, d = args[0].split('/')
                self.n = int(n)
                self.d = int(d)
            else:
                self.n = int(args[0])
                self.d = 1

        # int
        elif len(args) == 1 and isinstance(args[0], int):
            self.n = args[0]
            self.d = 1

        # n, d
        elif len(args) == 2:
            self.n = int(args[0])
            self.d = int(args[1])

        else:
            raise ValueError("Неправильні аргументи")

        if self.d == 0:
            raise ZeroDivisionError("Знаменник не може бути 0")

        self._reduce()

    # Скорочення дробу
    def _reduce(self):
        g = gcd(self.n, self.d)
        self.n //= g
        self.d //= g

        if self.d < 0:
            self.n *= -1
            self.d *= -1

    def _to_rational(self, other):
        if isinstance(other, Rational):
            return other
        if isinstance(other, int):
            return Rational(other)
        raise TypeError("Потрібно Rational або int")

    # +
    def __add__(self, other):
        other = self._to_rational(other)
        return Rational(
            self.n * other.d + other.n * self.d,
            self.d * other.d
        )

    # -
    def __sub__(self, other):
        other = self._to_rational(other)
        return Rational(
            self.n * other.d - other.n * self.d,
            self.d * other.d
        )

    # *
    def __mul__(self, other):
        other = self._to_rational(other)
        return Rational(self.n * other.n, self.d * other.d)

    # /
    def __truediv__(self, other):
        other = self._to_rational(other)

        if other.n == 0:
            raise ZeroDivisionError("Ділення на нуль")

        return Rational(self.n * other.d, self.d * other.n)

    # float()
    def __call__(self):
        return self.n / self.d

    # []
    def __getitem__(self, key):
        if key == "n":
            return self.n
        if key == "d":
            return self.d
        raise KeyError("Ключі: n або d")

    def __setitem__(self, key, value):
        if key == "n":
            self.n = value
        elif key == "d":
            if value == 0:
                raise ZeroDivisionError("Знаменник не може бути 0")
            self.d = value
        else:
            raise KeyError("Ключі: n або d")

        self._reduce()

    def __str__(self):
        return str(self.n) if self.d == 1 else f"{self.n}/{self.d}"


# =====================================================
# Клас RationalList
# =====================================================

class RationalList:

    def __init__(self, elements=None):
        self.data = []

        if elements is not None:
            for el in elements:
                self.append(el)

    def append(self, value):
        if isinstance(value, Rational):
            self.data.append(value)
        elif isinstance(value, int):
            self.data.append(Rational(value))
        else:
            raise TypeError("Тільки Rational або int")

    def __getitem__(self, index):
        return self.data[index]

    def __setitem__(self, index, value):
        if isinstance(value, Rational):
            self.data[index] = value
        elif isinstance(value, int):
            self.data[index] = Rational(value)
        else:
            raise TypeError("Потрібно Rational або int")

    def __len__(self):
        return len(self.data)

    def __add__(self, other):
        new_list = RationalList(self.data)

        if isinstance(other, RationalList):
            for el in other.data:
                new_list.append(el)
        else:
            new_list.append(other)

        return new_list

    def __iadd__(self, other):
        if isinstance(other, RationalList):
            for el in other.data:
                self.append(el)
        else:
            self.append(other)

        return self

    def __str__(self):
        return "[" + ", ".join(str(x) for x in self.data) + "]"

    def sum(self):
        s = Rational(0)
        for el in self.data:
            s = s + el
        return s


# =====================================================
# Зчитування з файлу
# =====================================================

def load_rational_list(file_name):
    r_list = RationalList()

    with open(file_name, "r", encoding="utf-8") as f:
        for line in f:
            for num in line.split():
                if '/' in num:
                    r_list += Rational(num)
                else:
                    r_list += int(num)

    return r_list


# =====================================================
# Основна програма
# =====================================================

files = ["input01.txt", "input02.txt", "input03.txt"]

for file_name in files:

    try:
        numbers = load_rational_list(file_name)
        total = numbers.sum()

        print("=" * 50)
        print("Файл:", file_name)
        print("Список:", numbers)
        print("Кількість елементів:", len(numbers))
        print("Сума:", total)
        print("Десятковий вигляд:", total())

    except FileNotFoundError:
        print(f"Файл {file_name} не знайдено")

    except Exception as e:
        print(f"Помилка у файлі {file_name}: {e}")
