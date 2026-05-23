import math


# ================= BASE CLASS =================

class Figure:
    def dimension(self):
        return 0

    def perimetr(self):
        return None

    def square(self):
        return None

    def squareSurface(self):
        return None

    def squareBase(self):
        return None

    def height(self):
        return None

    def volume(self):
        return None


# ================= 2D FIGURES =================

class Triangle(Figure):
    def __init__(self, a, b, c):
        self.a, self.b, self.c = a, b, c

        if (a + b <= c) or (a + c <= b) or (b + c <= a):
            self.valid = False
        else:
            self.valid = True

    def dimension(self):
        return 2

    def perimetr(self):
        return self.a + self.b + self.c

    def square(self):
        if not self.valid:
            return 0 

        p = self.perimetr() / 2
        val = p * (p - self.a) * (p - self.b) * (p - self.c)

        if val < 0:
            return 0

        return math.sqrt(val)

    def volume(self):
        return self.square()


class Rectangle(Figure):
    def __init__(self, a, b):
        self.a, self.b = a, b

    def dimension(self):
        return 2

    def perimetr(self):
        return 2 * (self.a + self.b)

    def square(self):
        return self.a * self.b

    def volume(self):
        return self.square()


class Trapeze(Figure):
    def __init__(self, a, b, c, d):
        self.a, self.b, self.c, self.d = a, b, c, d

    def dimension(self):
        return 2

    def perimetr(self):
        return self.a + self.b + self.c + self.d

    def square(self):
        # без висоти (якщо не дана) — Геронова апроксимація не задана,
        # тому беремо спрощення: середня основа * висота немає → умовно
        return (self.a + self.b) / 2 * abs(self.c - self.d)

    def volume(self):
        return self.square()


class Parallelogram(Figure):
    def __init__(self, a, b, h):
        self.a, self.b, self.h = a, b, h

    def dimension(self):
        return 2

    def perimetr(self):
        return 2 * (self.a + self.b)

    def square(self):
        return self.a * self.h

    def volume(self):
        return self.square()


class Circle(Figure):
    def __init__(self, r):
        self.r = r

    def dimension(self):
        return 2

    def perimetr(self):
        return 2 * math.pi * self.r

    def square(self):
        return math.pi * self.r ** 2

    def volume(self):
        return self.square()


# ================= 3D FIGURES =================

class Ball(Circle):
    def dimension(self):
        return 3

    def squareSurface(self):
        return 4 * math.pi * self.r ** 2

    def volume(self):
        return (4/3) * math.pi * self.r ** 3


class Cone(Circle):
    def __init__(self, r, h):
        super().__init__(r)
        self.h = h

    def dimension(self):
        return 3

    def squareSurface(self):
        l = math.sqrt(self.r**2 + self.h**2)
        return math.pi * self.r * (self.r + l)

    def squareBase(self):
        return super().square()

    def height(self):
        return self.h

    def volume(self):
        return (1/3) * math.pi * self.r**2 * self.h


class RectangularParallelepiped(Rectangle):
    def __init__(self, a, b, c):
        super().__init__(a, b)
        self.c = c

    def dimension(self):
        return 3

    def squareSurface(self):
        return 2 * (self.a*self.b + self.a*self.c + self.b*self.c)

    def squareBase(self):
        return super().square()

    def height(self):
        return self.c

    def volume(self):
        return self.a * self.b * self.c


class TriangularPrism(Triangle):
    def __init__(self, a, b, c, h):
        super().__init__(a, b, c)
        self.h = h

    def dimension(self):
        return 3

    def squareBase(self):
        return super().square()

    def height(self):
        return self.h

    def squareSurface(self):
        return 2 * self.squareBase() + self.perimetr() * self.h

    def volume(self):
        return self.squareBase() * self.h


class TriangularPyramid(Triangle):
    def __init__(self, a, h):
        self.a = a
        self.h = h

    def dimension(self):
        return 3

    def squareBase(self):
        return (math.sqrt(3)/4) * self.a**2

    def height(self):
        return self.h

    def volume(self):
        return (1/3) * self.squareBase() * self.h


class QuadrangularPyramid(Rectangle):
    def __init__(self, a, b, h):
        super().__init__(a, b)
        self.h = h

    def dimension(self):
        return 3

    def squareBase(self):
        return super().square()

    def height(self):
        return self.h

    def volume(self):
        return (1/3) * self.squareBase() * self.h


# ================= PARSER =================

def create_figure(line):
    line = line.strip()
    if not line:
        return None

    data = line.split()
    name = data[0]

    try:
        if name == "Triangle":
            return Triangle(*map(float, data[1:]))

        if name == "Rectangle":
            return Rectangle(*map(float, data[1:]))

        if name == "Trapeze":
            return Trapeze(*map(float, data[1:]))

        if name == "Parallelogram":
            return Parallelogram(*map(float, data[1:]))

        if name == "Circle":
            return Circle(float(data[1]))

        if name == "Ball":
            return Ball(float(data[1]))

        if name == "Cone":
            return Cone(*map(float, data[1:]))

        if name == "RectangularParallelepiped":
            return RectangularParallelepiped(*map(float, data[1:]))

        if name == "TriangularPrism":
            return TriangularPrism(*map(float, data[1:]))

        if name == "TriangularPyramid":
            return TriangularPyramid(*map(float, data[1:]))

        if name == "QuadrangularPyramid":
            return QuadrangularPyramid(*map(float, data[1:]))

    except Exception as e:
        print("Ошибка:", line)
        print(e)

    return None


# ================= MAIN =================

if __name__ == "__main__":

    files = ["input01.txt", "input02.txt", "input03.txt"]

    max_value = float("-inf")
    max_fig = None

    for fname in files:
        try:
            with open(fname, "r", encoding="utf-8") as f:
                print("\n---", fname, "---")

                for line in f:
                    fig = create_figure(line)
                    if fig is None:
                        continue

                    v = fig.volume()
                    print(type(fig).__name__, "=", v)

                    if v > max_value:
                        max_value = v
                        max_fig = fig

        except FileNotFoundError:
            print("Файл не найден:", fname)

    print("\n===== RESULT =====")

    if max_fig:
        print("MAX =", max_value)
        print("FIGURE =", type(max_fig).__name__)
    else:
        print("Нет корректных фигур")
