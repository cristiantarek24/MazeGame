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
    level = levels[level_index]
    level.draw(pen, player)

    window.listen()
    window.onkey(lambda: player.go_up(level.walls), "Up")
    window.onkey(lambda: player.go_down(level.walls), "Down")
    window.onkey(lambda: player.go_left(level.walls), "Left")
    window.onkey(lambda: player.go_right(level.walls), "Right")



    turtle.done()


if __name__ == "__main__":
    main()