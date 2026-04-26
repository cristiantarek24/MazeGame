import sys
import os
import turtle
import tkinter as tk
import subprocess
from Maze import levels, Pen, Player, EndPoint
from search_algorithms import bfs, dfs, astar, maze_to_grid, find_start_goal, grid_to_screen


# Enables or disables all solver buttons at once.
# Called to prevent the player from triggering a new solve while one is running.
def _set_buttons_state(buttons, state):
    for btn in buttons:
        btn.configure(state=state)


# Creates and places the three algorithm buttons (BFS, DFS, A*) at the
# bottom of the turtle window, each with its own color and hover effect.
def _add_solver_buttons(window, solve_fn_map):
    canvas = window.getcanvas()
    root   = canvas.winfo_toplevel()
    frame  = tk.Frame(root, bg="#050816", pady=6)
    frame.place(relx=0.5, rely=1.0, anchor="s")

    styles  = [("#1e40af", "#1d4ed8"), ("#065f46", "#047857"), ("#78350f", "#92400e")]
    labels  = ["⚙ BFS", "⚙ DFS", "⚙ A*"]
    buttons = []

    for (bg, hover), label, (_, fn) in zip(styles, labels, solve_fn_map.items()):
        btn = tk.Button(
            frame, text=label, command=fn,
            bg=bg, fg="white", activebackground=hover, activeforeground="white",
            relief="flat", bd=0, highlightthickness=0,
            padx=18, pady=6, cursor="hand2", font=("Arial", 11, "bold"),
        )
        btn.bind("<Enter>", lambda e, b=btn, h=hover: b.configure(bg=h))
        btn.bind("<Leave>", lambda e, b=btn, c=bg:   b.configure(bg=c))
        btn.pack(side="left", padx=8)
        buttons.append(btn)

    return buttons


# Moves the player one step along the solved path, then schedules the next
# step after step_ms milliseconds. Re-enables buttons and triggers win
# detection when the last step is reached.
def _animate_path(window, player, path, idx, win_shown, check_win_fn,
                  solver_buttons, step_ms=60):
    if idx >= len(path):
        check_win_fn()
        _set_buttons_state(solver_buttons, "normal")
        return
    row, col = path[idx]
    player.goto(-288 + col * 24, 288 - row * 24)
    window.update()
    window.ontimer(
        lambda: _animate_path(window, player, path, idx + 1,
                              win_shown, check_win_fn, solver_buttons, step_ms),
        step_ms
    )


# Builds and displays the win popup with three actions:
# Play Again resets the maze, Choose Another Level returns to main menu,
# and Exit closes the game entirely.
def show_win_popup(window, pen, player, endpoint_turtle, level, level_index,
                   win_shown, solver_buttons):

    canvas = window.getcanvas()
    root   = canvas.winfo_toplevel()

    popup = tk.Toplevel(root)
    popup.title("You Escaped!")
    popup.configure(bg="#050816")
    popup.resizable(False, False)
    popup.grab_set()

    W, H = 360, 340
    rx = root.winfo_x() + (root.winfo_width()  - W) // 2
    ry = root.winfo_y() + (root.winfo_height() - H) // 2
    popup.geometry(f"{W}x{H}+{rx}+{ry}")

    card = tk.Frame(popup, bg="#0f1829",
                    highlightthickness=2, highlightbackground="#f59e0b", bd=0)
    card.place(relx=0.5, rely=0.5, anchor="center", width=320, height=310)

    tk.Label(card, text="🏆", font=("Arial", 46),
             bg="#0f1829", fg="gold").pack(pady=(18, 0))
    tk.Label(card, text="YOU ESCAPED!", font=("Arial", 20, "bold"),
             bg="#0f1829", fg="#ffffff").pack(pady=(0, 2))
    tk.Label(card, text="The maze bows before you.",
             font=("Arial", 10, "italic"), bg="#0f1829", fg="#64748b").pack(pady=(0, 16))

    # Builds a styled dark-theme button with a hover color transition.
    def make_btn(parent, text, command, bg="#1e2d50", hover="#2d4070"):
        btn = tk.Button(
            parent, text=text, command=command,
            bg=bg, fg="#ffffff", activebackground=hover, activeforeground="#ffffff",
            relief="flat", bd=0, highlightthickness=0,
            padx=0, pady=10, cursor="hand2", font=("Arial", 12, "bold"), width=22,
        )
        btn.bind("<Enter>", lambda _: btn.configure(bg=hover))
        btn.bind("<Leave>", lambda _: btn.configure(bg=bg))
        return btn

    # Resets the maze and player back to the starting state without closing the window.
    def play_again():
        win_shown[0] = False
        popup.destroy()
        window.tracer(0)
        pen.clearstamps()
        level.draw(pen, player, endpoint_turtle)
        window.update()
        window.tracer(1)
        _set_buttons_state(solver_buttons, "normal")

    # Closes the game window and signals main.py to show the level select menu.
    def choose_level():
        popup.destroy()
        window.getcanvas().winfo_toplevel().destroy()
        sys.exit(2)

    # Closes the game window and terminates the process completely.
    def exit_game():
        popup.destroy()
        window.getcanvas().winfo_toplevel().destroy()
        sys.exit(0)

    btn_frame = tk.Frame(card, bg="#0f1829")
    btn_frame.pack()
    make_btn(btn_frame, "▶   Play Again",           play_again,
             bg="#7c3aed", hover="#6d28d9").pack(pady=4)
    make_btn(btn_frame, "Choose Another Level", choose_level,
             bg="#1e2d50", hover="#2d4070").pack(pady=4)
    make_btn(btn_frame, "✕   Exit",                  exit_game,
             bg="#450a0a", hover="#7f1d1d").pack(pady=4)


# Entry point: loads the selected level, draws the maze, sets up keyboard
# controls, builds the solver buttons, and starts the turtle event loop.
def main():
    level_index = int(sys.argv[1])

    window = turtle.Screen()
    window.bgcolor("#050816")
    window.title("Escape the Maze")
    window.setup(width=700, height=740)

    pen             = Pen()
    player          = Player()
    endpoint_turtle = EndPoint()

    level = levels[level_index]

    window.tracer(0)
    level.draw(pen, player, endpoint_turtle)
    window.update()
    window.tracer(1)

    grid              = maze_to_grid(level.grid)
    start_rc, goal_rc = find_start_goal(level.grid)

    win_shown      = [False]
    solver_buttons = []

    # Checks if the player's current position matches the exit cell.
    # If so, disables the solver buttons and shows the win popup.
    def check_win():
        if win_shown[0] or level.endpoint is None:
            return
        if (round(player.xcor()), round(player.ycor())) == level.endpoint:
            win_shown[0] = True
            _set_buttons_state(solver_buttons, "disabled")
            show_win_popup(window, pen, player, endpoint_turtle,
                           level, level_index, win_shown, solver_buttons)

    # Wraps a player movement action with a win check after each step.
    # Ignores input if the game is already won.
    def move(action):
        if win_shown[0]:
            return
        action()
        check_win()

    window.listen()
    window.onkey(lambda: move(lambda: player.go_up(level.walls)),    "Up")
    window.onkey(lambda: move(lambda: player.go_down(level.walls)),  "Down")
    window.onkey(lambda: move(lambda: player.go_left(level.walls)),  "Left")
    window.onkey(lambda: move(lambda: player.go_right(level.walls)), "Right")

    # Resets the player to the start position, runs the chosen algorithm to
    # find a path, then animates the player moving along that path.
    def run_solver(algorithm_fn):
        if win_shown[0]:
            return
        player.goto(grid_to_screen(start_rc[0], start_rc[1]))
        window.update()
        path = algorithm_fn(grid, start_rc, goal_rc)
        if not path:
            return
        _set_buttons_state(solver_buttons, "disabled")
        _animate_path(window, player, path, 1,
                      win_shown, check_win, solver_buttons)

    solve_map = {
        "BFS": lambda: run_solver(bfs),
        "DFS": lambda: run_solver(dfs),
        "A*":  lambda: run_solver(astar),
    }
    solver_buttons.extend(_add_solver_buttons(window, solve_map))

    turtle.done()


if __name__ == "__main__":
    main()