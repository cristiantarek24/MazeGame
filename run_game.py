import sys
import turtle

from Maze import levels, Pen, Player


def main():
    level_index = int(sys.argv[1])

    window = turtle.Screen()
    window.bgcolor("#050816")
    window.title("Escape the Maze")
    window.setup(width=700, height=700)

    pen = Pen()
    player = Player()
    levels[level_index].draw(pen, player)

    window.listen()
    window.onkey(player.go_up, "Up")
    window.onkey(player.go_down, "Down")
    window.onkey(player.go_left, "Left")
    window.onkey(player.go_right, "Right")

    turtle.done()


if __name__ == "__main__":
    main()