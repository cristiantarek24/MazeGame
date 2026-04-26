import sys
import pygame
import os
import turtle
import tkinter as tk
from Maze import levels, Pen, Player, EndPoint
from search_algorithms import bfs, dfs, astar, maze_to_grid, find_start_goal, grid_to_screen

def _set_buttons_state(buttons, state):
    for btn in buttons:
        btn.configure(state=state)

def _add_solver_buttons(window, solve_fn_map):
    canvas = window.getcanvas()
    root = canvas.winfo_toplevel()
    frame = tk.Frame(root, bg="#050816", pady=6)
    frame.place(relx=0.5, rely=1.0, anchor="s")

    styles = [("#1e40af", "#1d4ed8"), ("#065f46", "#047857"), ("#78350f", "#92400e")]
    labels = ["⚙ BFS", "⚙ DFS", "⚙ A*"]
    buttons = []

    for (bg, hover), label, (_, fn) in zip(styles, labels, solve_fn_map.items()):
        btn = tk.Button(
            frame, text=label, command=fn,
            bg=bg, fg="white", activebackground=hover, activeforeground="white",
            relief="flat", bd=0, highlightthickness=0,
            padx=18, pady=6, cursor="hand2", font=("Arial", 11, "bold"),
        )
        btn.bind("<Enter>", lambda e, b=btn, h=hover: b.configure(bg=h))
        btn.bind("<Leave>", lambda e, b=btn, c=bg: b.configure(bg=c))
        btn.pack(side="left", padx=8)
        buttons.append(btn)
    return buttons

def _animate_path(window, player, path, idx, win_shown, check_win_fn, solver_buttons, step_ms=60):
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

def show_win_popup(window, pen, player, endpoint_turtle, level, level_index, win_shown, solver_buttons):
    root = window.getcanvas().winfo_toplevel()
    popup = tk.Toplevel(root)
    popup.title("You Escaped!")
    popup.configure(bg="#050816")
    popup.grab_set()

    W, H = 360, 340
    rx = root.winfo_x() + (root.winfo_width() - W) // 2
    ry = root.winfo_y() + (root.winfo_height() - H) // 2
    popup.geometry(f"{W}x{H}+{rx}+{ry}")

    card = tk.Frame(popup, bg="#0f1829", highlightthickness=2, highlightbackground="#f59e0b", bd=0)
    card.place(relx=0.5, rely=0.5, anchor="center", width=320, height=310)

    tk.Label(card, text="🏆", font=("Arial", 46), bg="#0f1829", fg="gold").pack(pady=(18, 0))
    tk.Label(card, text="YOU ESCAPED!", font=("Arial", 20, "bold"), bg="#0f1829", fg="#ffffff").pack()

    def play_again():
        win_shown[0] = False
        popup.destroy()
        pygame.mixer.music.play(-1)
        window.tracer(0)
        pen.clearstamps()
        level.draw(pen, player, endpoint_turtle)
        window.update()
        window.tracer(1)
        _set_buttons_state(solver_buttons, "normal")

    def exit_game():
        pygame.mixer.music.stop()
        popup.destroy()
        window.getcanvas().winfo_toplevel().destroy()
        sys.exit(0)

    def choose_level():
        pygame.mixer.music.stop()
        popup.destroy()
        window.getcanvas().winfo_toplevel().destroy()
        sys.exit(2)

    tk.Button(card, text="Play Again", command=play_again, bg="#7c3aed", fg="white", width=22, pady=10).pack(pady=4)
    tk.Button(card, text="Choose Level", command=choose_level, bg="#1e2d50", fg="white", width=22, pady=10).pack(pady=4)
    tk.Button(card, text="Exit", command=exit_game, bg="#450a0a", fg="white", width=22, pady=10).pack(pady=4)

def main():
    pygame.mixer.init()
    pygame.mixer.music.load(os.path.join("game.mp3"))
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1)

    step_sound = pygame.mixer.Sound(os.path.join("step.wav"))
    step_sound.set_volume(0.1)

    win_sound = pygame.mixer.Sound(os.path.join("win.wav"))
    win_sound.set_volume(0.8)

    if len(sys.argv) < 2:
        return
    level_index = int(sys.argv[1])

    window = turtle.Screen()
    window.bgcolor("#050816")
    window.title("Escape the Maze")
    window.setup(width=700, height=740)



    window.register_shape("elf_side01_idle.gif")
    window.register_shape("elf_side02_idle.gif")
    window.register_shape("door.gif")
    window.register_shape("Block.gif")

    pen = Pen()
    player = Player()
    endpoint_turtle = EndPoint()
    level = levels[level_index]

    window.tracer(0)
    level.draw(pen, player, endpoint_turtle)
    window.update()
    window.tracer(1)

    grid = maze_to_grid(level.grid)
    start_rc, goal_rc = find_start_goal(level.grid)
    win_shown = [False]
    solver_buttons = []

    def check_win():
        if not win_shown[0] and level.endpoint:
            if (round(player.xcor()), round(player.ycor())) == level.endpoint:
                win_shown[0] = True
                pygame.mixer.music.stop()
                win_sound.play()
                _set_buttons_state(solver_buttons, "disabled")
                show_win_popup(window, pen, player, endpoint_turtle, level, level_index, win_shown, solver_buttons)

    def move(action):
        if not win_shown[0]:
            prev = (round(player.xcor()), round(player.ycor()))
            action()
            if (round(player.xcor()), round(player.ycor())) != prev:
                step_sound.play()
            check_win()

    window.listen()
    window.onkey(lambda: move(lambda: player.go_up(level.walls)), "Up")
    window.onkey(lambda: move(lambda: player.go_down(level.walls)), "Down")
    window.onkey(lambda: move(lambda: player.go_left(level.walls)), "Left")
    window.onkey(lambda: move(lambda: player.go_right(level.walls)), "Right")

    def run_solver(algorithm_fn):
        if win_shown[0]: return
        player.goto(grid_to_screen(start_rc[0], start_rc[1]))
        window.update()
        path = algorithm_fn(grid, start_rc, goal_rc)
        if path:
            _set_buttons_state(solver_buttons, "disabled")
            _animate_path(window, player, path, 1, win_shown, check_win, solver_buttons)

    solve_map = {
        "BFS": lambda: run_solver(bfs),
        "DFS": lambda: run_solver(dfs),
        "A*": lambda: run_solver(astar),
    }
    solver_buttons.extend(_add_solver_buttons(window, solve_map))
    turtle.done()

if __name__ == "__main__":
    main()