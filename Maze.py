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

    def _can_move(self, x, y, walls):
        return (round(x), round(y)) not in walls

    def go_up(self, walls):
        new_y = self.ycor() + 24
        if self._can_move(self.xcor(), new_y, walls):
            self.goto(self.xcor(), new_y)

    def go_down(self, walls):
        new_y = self.ycor() - 24
        if self._can_move(self.xcor(), new_y, walls):
            self.goto(self.xcor(), new_y)

    def go_left(self, walls):
        new_x = self.xcor() - 24
        if self._can_move(new_x, self.ycor(), walls):
            self.goto(new_x, self.ycor())

    def go_right(self, walls):
        new_x = self.xcor() + 24
        if self._can_move(new_x, self.ycor(), walls):
            self.goto(new_x, self.ycor())

# Holds a maze grid and converts it to turtle screen coordinates
class Level:
    CELL_SIZE = 24

    def __init__(self, grid):
        self.grid = grid
        self.walls = set()

    def draw(self, pen, player=None):
        self.walls.clear()
        for y, row in enumerate(self.grid):
            for x, char in enumerate(row):
                screen_x = -288 + (x * self.CELL_SIZE)
                screen_y = 288 - (y * self.CELL_SIZE)
                if char == "X":
                    pen.goto(screen_x, screen_y)
                    pen.stamp()
                    self.walls.add((round(screen_x), round(screen_y)))
                if char == "P" and player is not None:
                    player.goto(screen_x, screen_y)
walls = []



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

