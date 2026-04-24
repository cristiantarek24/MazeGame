import turtle

from Maze import Pen, Player, level_setup, levels

window = turtle.Screen()
window.bgcolor("black")
window.title("Escape the Maze")
window.setup(width=700, height=700)

maze_pen = Pen()
player = Player()

level_setup(levels[0], maze_pen, player)

turtle.done()