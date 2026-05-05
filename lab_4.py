import turtle

# ================= BASE =================

class Figure:
    def init(self):
        self.x = 0
        self.y = 0
        self.visible = False

    def setPosition(self, x, y):
        self.x = x
        self.y = y

    def draw(self, color):
        pass 

    def show(self):
        self.visible = True
        self.draw("black")

    def hide(self):
        self.visible = False
        turtle.clear()


# ================= FIGURES =================

class Cross(Figure):
    def draw(self, color):
        turtle.penup()
        turtle.goto(self.x - 30, self.y - 30)
        turtle.pendown()
        turtle.color(color)

        turtle.goto(self.x + 30, self.y + 30)
        turtle.penup()
        turtle.goto(self.x - 30, self.y + 30)
        turtle.pendown()
        turtle.goto(self.x + 30, self.y - 30)
        turtle.penup()


class Zero(Figure):
    def draw(self, color):
        turtle.penup()
        turtle.goto(self.x, self.y - 30)
        turtle.pendown()
        turtle.color(color)
        turtle.circle(30)
        turtle.penup()


class Board(Figure):
    def draw(self, color):
        turtle.color(color)


        for x in [-100, 0, 100]:
            turtle.penup()
            turtle.goto(x, -150)
            turtle.pendown()
            turtle.goto(x, 150)


        for y in [-100, 0, 100]:
            turtle.penup()
            turtle.goto(-150, y)
            turtle.pendown()
            turtle.goto(150, y)

        turtle.penup()


# ================= GAME =================

board_state = [[None]*3 for _ in range(3)]
current_player = "X"


def get_cell(x, y):
    col = int((x + 150) // 100)
    row = int((150 - y) // 100)

    if 0 <= row < 3 and 0 <= col < 3:
        return row, col
    return None


def cell_center(row, col):
    x = -100 + col*100
    y = 100 - row*100
    return x, y


def check_winner():

    for row in board_state:
        if row[0] and row[0] == row[1] == row[2]:
            return row[0]


    for c in range(3):
        if board_state[0][c] and board_state[0][c] == board_state[1][c] == board_state[2][c]:
            return board_state[0][c]


    if board_state[0][0] and board_state[0][0] == board_state[1][1] == board_state[2][2]:
        return board_state[0][0]

    if board_state[0][2] and board_state[0][2] == board_state[1][1] == board_state[2][0]:
        return board_state[0][2]

    return None


def on_click(x, y):
    global current_player

    cell = get_cell(x, y)
    if not cell:
        return

    row, col = cell

    if board_state[row][col] is not None:
        return

    cx, cy = cell_center(row, col)

    if current_player == "X":
        fig = Cross()
        board_state[row][col] = "X"
        current_player = "O"
    else:
        fig = Zero()
        board_state[row][col] = "O"
        current_player = "X"

    fig.setPosition(cx, cy)
    fig.show()

    winner = check_winner()
    if winner:
        print("WINNER:", winner)
        turtle.bye()


# ================= MAIN =================

turtle.speed(0)
turtle.hideturtle()

board = Board()
board.show()

turtle.onscreenclick(on_click)
turtle.listen()

turtle.mainloop()
