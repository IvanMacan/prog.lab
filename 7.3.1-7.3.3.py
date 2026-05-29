# ============================================================
# 7.3.1–7.3.3 Rational + RationalList + виключення
# ============================================================

from math import gcd


# ============================================================
# Виключення
# ============================================================

class RationalError(ZeroDivisionError):
    def __init__(self, message="Знаменник не може дорівнювати нулю"):
        super().__init__(message)


class RationalValueError(Exception):
    def __init__(self, message="Некоректні дані для Rational"):
        super().__init__(message)


# ============================================================
# Rational
# ============================================================

class Rational:
    def __init__(self, n, d=1):

        if d == 0:
            raise RationalError()

        if not isinstance(n, int) or not isinstance(d, int):
            raise RationalValueError()

        # скорочення дробу
        g = gcd(n, d)
        n //= g
        d //= g

        # нормалізація знаку
        if d < 0:
            n *= -1
            d *= -1

        self.n = n
        self.d = d

    def __add__(self, other):
        if not isinstance(other, Rational):
            raise RationalValueError("Можна додавати тільки Rational")

        return Rational(
            self.n * other.d + other.n * self.d,
            self.d * other.d
        )

    def value(self):
        return self.n / self.d


# ============================================================
# RationalList
# ============================================================

class RationalList:
    def __init__(self):
        self.data = []

    def add(self, value):
        if not isinstance(value, Rational):
            raise RationalValueError("Дозволено тільки Rational")

        self.data.append(value)

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        return iter(self.data)

    def sum(self):
        res = Rational(0, 1)
        for x in self.data:
            res = res + x
        return res

    def __str__(self):
        return "[" + ", ".join(f"{x.n}/{x.d}" for x in self.data) + "]"


# ============================================================
# Завантаження з файлу
# ============================================================

def parse_rational(token):
    if "/" in token:
        n, d = map(int, token.split("/"))
        return Rational(n, d)
    return Rational(int(token), 1)


def load_rational_list(file_name):
    r_list = RationalList()

    with open(file_name, "r", encoding="utf-8") as f:
        for line in f:
            for num in line.split():
                r_list.add(parse_rational(num))

    return r_list


# ============================================================
# MAIN
# ============================================================

files = ["input01.txt", "input02.txt", "input03.txt"]

for file_name in files:

    try:
        numbers = load_rational_list(file_name)

        total = numbers.sum()

        print("=" * 40)
        print("Файл:", file_name)
        print("Список:", numbers)
        print("Кількість:", len(numbers))
        print("Сума:", f"{total.n}/{total.d}")
        print("Десяткове:", total.value())

    except FileNotFoundError:
        print("Файл не знайдено:", file_name)

    except RationalValueError as e:
        print("RationalValueError:", e)

    except RationalError as e:
        print("RationalError:", e)
