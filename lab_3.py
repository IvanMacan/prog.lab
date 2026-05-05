import math

class Figure:
    def dimention(self):
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


# ================= 2D =================

class Rectangle(Figure):
    def init(self, a, b):
        self.a = a
        self.b = b

    def dimention(self):
        return 2

    def perimetr(self):
        return 2 * (self.a + self.b)

    def square(self):
        return self.a * self.b

    def volume(self):
        return self.square()


class Circle(Figure):
    def init(self, r):
        self.r = r

    def dimention(self):
        return 2

    def perimetr(self):
        return 2 * math.pi * self.r

    def square(self):
        return math.pi * self.r ** 2

    def volume(self):
        return self.square()


class Triangle(Figure):
    def init(self, a, b, c):
        self.a, self.b, self.c = a, b, c

    def dimention(self):
        return 2

    def perimetr(self):
        return self.a + self.b + self.c

    def square(self):
        p = self.perimetr() / 2
        return math.sqrt(p * (p - self.a) * (p - self.b) * (p - self.c))

    def volume(self):
        return self.square()


class Parallelogram(Figure):
    def init(self, a, b, h):
        self.a, self.b, self.h = a, b, h

    def dimention(self):
        return 2

    def perimetr(self):
        return 2 * (self.a + self.b)

    def square(self):
        return self.a * self.h

    def volume(self):
        return self.square()


# ================= 3D =================

class RectangularParallelepiped(Rectangle):
    def init(self, a, b, c):
        super().init(a, b)
        self.c = c

    def dimention(self):
        return 3

    def squareSurface(self):
        return 2 * (self.a*self.b + self.a*self.c + self.b*self.c)

    def squareBase(self):
        return super().square()

    def height(self):
        return self.c

    def volume(self):
        return self.a * self.b * self.c


class Sphere(Circle):
    def dimention(self):
        return 3

    def squareSurface(self):
        return 4 * math.pi * self.r**2

    def volume(self):
        return (4/3) * math.pi * self.r**3


class Cone(Circle):
    def init(self, r, h):
        super().init(r)
        self.h = h

    def dimention(self):
        return 3

    def squareSurface(self):
        l = math.sqrt(self.r**2 + self.h**2)
        return math.pi*self.r*(self.r + l)

    def squareBase(self):
        return super().square()

    def height(self):
        return self.h

    def volume(self):
        return (1/3) * self.squareBase() * self.h


class TriangularPrism(Triangle):
    def init(self, a, b, c, h):
        super().init(a, b, c)
        self.h = h

    def dimention(self):
        return 3

    def squareBase(self):
        return super().square()

    def height(self):
        return self.h

    def squareSurface(self):
        return 2*self.squareBase() + self.perimetr()*self.h

    def volume(self):
        return self.squareBase() * self.h


# ================= MAIN =================

def create_figure(line):
    data = line.split()
    name = data[0]

    try:
        if name == "Rectangle":
            a, b = map(float, data[1:])
            return Rectangle(a, b)

        elif name == "Circle":
            r = float(data[1])
            return Circle(r)

        elif name == "Triangle":
            a, b, c = map(float, data[1:])
            return Triangle(a, b, c)

        elif name == "Parallelogram":
            a, b, h = map(float, data[1:])
            return Parallelogram(a, b, h)

        elif name == "RectangularParallelepiped":
            a, b, c = map(float, data[1:])
            return RectangularParallelepiped(a, b, c)

        elif name == "Sphere":
            r = float(data[1])
            return Sphere(r)

        elif name == "Cone":
            r, h = map(float, data[1:])
            return Cone(r, h)
        elif name == "TriangularPrism":
            a, b, c, h = map(float, data[1:])
            return TriangularPrism(a, b, c, h)

    except:
        print("Ошибка в строке:", line)

    return None


if __name__ == "__main__":

    files = ["input01.txt", "input02.txt", "input03.txt"]

    max_volume = 0
    max_figure = None

    for fname in files:
        try:
            with open(fname) as f:
                print(f"\n--- {fname} ---")

                for line in f:
                    fig = create_figure(line)

                    if fig is None:
                        continue

                    v = fig.volume()
                    print(type(fig).name, "=", v)

                    if v > max_volume:
                        max_volume = v
                        max_figure = fig

        except FileNotFoundError:
            print(f"Файл {fname} не найден")

    print("\n===== RESULT =====")
    print("MAX =", max_volume)
    print("FIGURE =", type(max_figure).name)
