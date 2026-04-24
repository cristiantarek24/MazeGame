import turtle


# Turtle used exclusively for stamping wall tiles; never draws lines
class Pen(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.penup()
        self.shape("square")
        self.color("white")
        self.speed(0)


# Represents the player character on the maze grid
class Player(turtle.Turtle):
    SHAPE = "square"
    COLOR = "blue"

    def __init__(self):
        super().__init__()
        self._configure_appearance()

    def _configure_appearance(self):
        self.shape(self.SHAPE)
        self.color(self.COLOR)
        self.penup()

    def go_up(self):
        self.goto(self.xcor(), self.ycor() + 24)

    def go_down(self):
        self.goto(self.xcor(), self.ycor() - 24)

    def go_left(self):
        self.goto(self.xcor() - 24, self.ycor())

    def go_right(self):
        self.goto(self.xcor() + 24, self.ycor())


# Holds a maze grid and converts it to turtle screen coordinates
class Level:
    CELL_SIZE = 24  # pixels per grid cell

    def __init__(self, grid):
        self.grid = grid

    # 'X' = wall tile, 'P' = player start position, ' ' = open path
    def draw(self, pen, player=None):
        for y, row in enumerate(self.grid):
            for x, char in enumerate(row):
                # Origin (-288, 288) centers a 25x26 grid in the 700x700 window
                screen_x = -288 + (x * self.CELL_SIZE)
                screen_y = 288 - (y * self.CELL_SIZE)
                if char == "X":
                    pen.goto(screen_x, screen_y)
                    pen.stamp()
                if char == "P" and player is not None:
                    player.goto(screen_x, screen_y)


# All playable levels; index matches the button order in the menu
levels = [
    Level([
        "XXXXXXXXXXXXXXXXXXXXXXXXX",
        "XP  X    X              X",
        "X  X    X               X",
        "X  X    X               X",
        "X       XXXXXXXXXXXXX   X",
        "XXXX                X   X",
        "X      XXXXXXXXXXXXXX   X",
        "X   XXXX                X",
        "X   X             X     X",
        "X   X             X     X",
        "X   X             X     X",
        "X   XXXXXXX       XXX   X",
        "X         X         X   X",
        "X   XXXXXXXXXXX     X   X",
        "X             X     X   X",
        "X   XXXXXXXXXXX     X   X",
        "X   X             XXXX  X",
        "X   XXXXXXXXXXX      X  X",
        "X             X      X  X",
        "X    XXXXXXXXXX      X  X",
        "X                    X  X",
        "XXXXXXXX    XXXXXXXXXX  X",
        "X      X    X           X",
        "X      XXXXXX           X",
        "X                       X",
        "XXXXXXXXXXXXXXXXXXXXXXXXX",
    ]),
    Level([
        "XXXXXXXXXXXXXXXXXXXXXXXXX",
        "XP     X        X       X",
        "X XXX XXXXXXXX  X  XXX  X",
        "X X   X      X  X    X  X",
        "X X XXXXXXXX X  X X  X  X",
        "X X        X X  X X  X  X",
        "X XXXXXXXX X X  X X  X  X",
        "X        X X X  X    X  X",
        "XXXXXXX  X X X  X XXXX  X",
        "X     X  X X X  X    X  X",
        "X XXX X  X X X  XXXX X  X",
        "X X   X  X X X       X  X",
        "X X XXXXX     XXXXXXXX  X",
        "X X     X X X X         X",
        "X XXXXX X X X X  XXXXXXXX",
        "X     X X X X X         X",
        "XXXXX X X X X XXXXXXX   X",
        "X   X X X X X       X   X",
        "X X X X X X XXXXXXX X   X",
        "X X   X   X         X   X",
        "X XXXXXXXX XXXXXX       X",
        "X        X       X X    X",
        "X XXXXXXXX XXXXX X XXXX X",
        "X          X     X      X",
        "XXXXXXXXXXXXXXXXXXXXXXXXX",
    ]),
    Level([
        "XXXXXXXXXXXXXXXXXXXXXXXXX",
        "XP   X     X     X     XX",
        "X X XXXX X XXXX X XXXX  X",
        "X X    X      X X    X  X",
        "X XXXX X XXXX XXXXXX X  X",
        "X    X X    X        X  X",
        "XXXX X XXXX X XXXX X X  X",
        "X    X    X X    X X X  X",
        "X XXXX XXXX X XXXX X X  X",
        "X X    X    X X    X X  X",
        "X X XXXX XXXX X XXXX X  X",
        "X X    X    X X    X X  X",
        "X XXXX X  XXX X XXXX X  X",
        "X    X X    X X    X X  X",
        "XXXX X XXXX X XXXX X X  X",
        "X    X    X X    X X X  X",
        "X XXXX XXXX X XXXX X X  X",
        "X X    X    X X    X X  X",
        "X X XXXX XXXX X XXXX X  X",
        "X X    X    X X    X X  X",
        "X XXXX X XXXX X XXXX X  X",
        "X    X X    X X    X X  X",
        "X XXXX X XXXX X XXXX X  X",
        "X            X     X    X",
        "XXXXXXXXXXXXXXXXXXXXXXXXX",
    ]),
]