import turtle
from Maze import Pen, level_setup, levels

window = turtle.Screen()
window.bgcolor("black")
window.title("Escape the Maze")
window.setup(width=700, height=700)

obj = Pen()
level_setup(levels[0], obj)

window.mainloop()