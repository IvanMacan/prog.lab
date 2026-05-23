from math import gcd


class Rational:
    def __init__(self, *args):
        # копирование
        if len(args) == 1 and isinstance(args[0], Rational):
            self.n = args[0].n
            self.d = args[0].d

        # строка "n/d"
        elif len(args) == 1 and isinstance(args[0], str):
            parts = args[0].split('/')
            if len(parts) != 2:
                raise ValueError("Неправильний формат дробу!")
            self.n = int(parts[0])
            self.d = int(parts[1])

        # два числа
        elif len(args) == 2:
            self.n = int(args[0])
            self.d = int(args[1])

        else:
            raise ValueError("Неправильні аргументи конструктора!")

        if self.d == 0:
            raise ZeroDivisionError("Знаменник не може бути 0!")

        self._reduce()

    def _reduce(self):
        g = gcd(self.n, self.d)
        self.n //= g
        self.d //= g

        if self.d < 0:
            self.n *= -1
            self.d *= -1

    def __str__(self):
        return f"{self.n}/{self.d}"

    def __repr__(self):
        return self.__str__()

    def __call__(self):
        return self.n / self.d

    # -------------------------
    # преобразование
    # -------------------------
    def _to_rational(self, other):
        if isinstance(other, Rational):
            return other
        if isinstance(other, int):
            return Rational(other, 1)
        if isinstance(other, str):
            return Rational(other)
        raise TypeError("Можно только Rational, int или 'n/d'")

    # -------------------------
    # операции
    # -------------------------
    def __add__(self, other):
        other = self._to_rational(other)
        return Rational(self.n * other.d + other.n * self.d,
                        self.d * other.d)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        other = self._to_rational(other)
        return Rational(self.n * other.d - other.n * self.d,
                        self.d * other.d)

    def __rsub__(self, other):
        other = self._to_rational(other)
        return other.__sub__(self)

    def __mul__(self, other):
        other = self._to_rational(other)
        return Rational(self.n * other.n,
                        self.d * other.d)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        other = self._to_rational(other)
        if other.n == 0:
            raise ZeroDivisionError("Ділення на нуль!")
        return Rational(self.n * other.d,
                        self.d * other.n)

    def __rtruediv__(self, other):
        other = self._to_rational(other)
        return other.__truediv__(self)

    # -------------------------
    # []
    # -------------------------
    def __getitem__(self, key):
        if key == "n":
            return self.n
        if key == "d":
            return self.d
        raise KeyError("Тільки 'n' або 'd'")

    def __setitem__(self, key, value):
        if key == "n":
            self.n = value
        elif key == "d":
            if value == 0:
                raise ZeroDivisionError()
            self.d = value
        else:
            raise KeyError("Тільки 'n' або 'd'")
        self._reduce()


# ==========================
# вычисление выражений
# ==========================
def calculate_expression(expr):
    parts = expr.split()
    new_parts = []

    for p in parts:
        if '/' in p:
            new_parts.append(f'Rational("{p}")')
        else:
            new_parts.append(p)

    return eval(" ".join(new_parts))


# ==========================
# main
# ==========================
file_name = "input01.txt"

try:
    with open(file_name, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            try:
                result = calculate_expression(line)

                print("Вираз:", line)
                print("Результат:", result)
                print("Десятковий вигляд:", result())
                print()

            except Exception as e:
                print("Помилка у виразі:", line)
                print(e)

except FileNotFoundError:
    print("Файл не знайдено!")
