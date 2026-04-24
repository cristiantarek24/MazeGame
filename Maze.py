import turtle

# Create the pen to draw
class Pen(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.penup()
        self.shape("square")
        self.color("white")
        self.speed(0)


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

# Create the levels
level1 = [
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
    "XXXXXXXXXXXXXXXXXXXXXXXXX"
]

levels = [level1]

def level_setup(level, pen, player=None):
    for y in range(len(level)):
        for x in range(len(level[y])):
            character = level[y][x]

            screen_x = -288 + (x * 24)
            screen_y = 288 - (y * 24)

            if character == "X":
                pen.goto(screen_x, screen_y)
                pen.stamp()
            if character == "P" and player is not None:
                player.goto(screen_x, screen_y)

pen = Pen()

