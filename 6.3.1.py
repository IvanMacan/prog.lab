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

        # Рядок
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

    def _reduce(self):

        g = gcd(self.n, self.d)

        self.n //= g
        self.d //= g

        if self.d < 0:
            self.n *= -1
            self.d *= -1

    def __str__(self):

        if self.d == 1:
            return str(self.n)

        return f"{self.n}/{self.d}"


# =====================================================
# Ітератор
# =====================================================

class RationalListIterator:

    def __init__(self, data):

        self.data = sorted(
            data,
            key=lambda x: (-x.d, -x.n)
        )

        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):

        if self.index >= len(self.data):
            raise StopIteration

        value = self.data[self.index]
        self.index += 1
        return value


# =====================================================
# Клас RationalList
# =====================================================

class RationalList:

    def __init__(self):

        self.data = []

    def append(self, value):

        if isinstance(value, Rational):
            self.data.append(value)

        elif isinstance(value, int):
            self.data.append(Rational(value))

        else:
            raise TypeError("Можна додавати лише Rational або int")

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

    def __iadd__(self, other):

        if isinstance(other, RationalList):

            for el in other.data:
                self.append(el)

        elif isinstance(other, (Rational, int)):
            self.append(other)

        else:
            raise TypeError("Неправильний тип")

        return self

    def __iter__(self):
        return RationalListIterator(self.data)

    def __str__(self):
        return "[" + ", ".join(str(x) for x in self.data) + "]"


# =====================================================
# Зчитування файлу
# =====================================================

def load_file(file_name):

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

        r_list = load_file(file_name)

        print("=" * 50)
        print("Файл:", file_name)
        print("Елементи у порядку спадання знаменників:")

        for x in r_list:
            print(x)

    except FileNotFoundError:
        print(f"Файл {file_name} не знайдено")

    except Exception as e:
        print(f"Помилка у файлі {file_name}: {e}")
