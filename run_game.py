import sys
import os
import turtle
import tkinter as tk
import subprocess
from Maze import levels, Pen, Player, EndPoint



def show_win_popup(window, pen, player, endpoint_turtle, level, level_index, win_shown):

    canvas = window.getcanvas()
    root = canvas.winfo_toplevel()

    popup = tk.Toplevel(root)
    popup.title("You Escaped!")
    popup.configure(bg="#050816")
    popup.resizable(False, False)
    popup.grab_set()   # make it modal

    W, H = 360, 340
    rx = root.winfo_x() + (root.winfo_width()  - W) // 2
    ry = root.winfo_y() + (root.winfo_height() - H) // 2
    popup.geometry(f"{W}x{H}+{rx}+{ry}")

    card = tk.Frame(
        popup,
        bg="#0f1829",
        highlightthickness=2,
        highlightbackground="#f59e0b",
        bd=0,
    )
    card.place(relx=0.5, rely=0.5, anchor="center", width=320, height=310)

    # Trophy emoji
    tk.Label(
        card,
        text="🏆",
        font=("Arial", 46),
        bg="#0f1829",
        fg="gold",
    ).pack(pady=(18, 0))

    # Headline
    tk.Label(
        card,
        text="YOU ESCAPED!",
        font=("Arial", 20, "bold"),
        bg="#0f1829",
        fg="#ffffff",
    ).pack(pady=(0, 2))

    # Sub-line
    tk.Label(
        card,
        text="The maze bows before you.",
        font=("Arial", 10, "italic"),
        bg="#0f1829",
        fg="#64748b",
    ).pack(pady=(0, 16))

    def make_btn(parent, text, command, bg="#1e2d50", hover="#2d4070"):
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            bg=bg,
            fg="#ffffff",
            activebackground=hover,
            activeforeground="#ffffff",
            relief="flat",
            bd=0,
            highlightthickness=0,
            padx=0,
            pady=10,
            cursor="hand2",
            font=("Arial", 12, "bold"),
            width=22,
        )
        btn.bind("<Enter>", lambda _: btn.configure(bg=hover))
        btn.bind("<Leave>", lambda _: btn.configure(bg=bg))
        return btn



    def play_again():
        win_shown[0] = False
        popup.destroy()
        window.tracer(0)
        pen.clearstamps()
        level.draw(pen, player, endpoint_turtle)
        window.update()
        window.tracer(1)

    def choose_level():
        popup.destroy()
        window.getcanvas().winfo_toplevel().destroy()
        sys.exit(2)

    def exit_game():
        popup.destroy()
        window.getcanvas().winfo_toplevel().destroy()
        sys.exit(0)


    btn_frame = tk.Frame(card, bg="#0f1829")
    btn_frame.pack()

    make_btn(btn_frame, "▶   Play Again",       play_again,   bg="#7c3aed", hover="#6d28d9").pack(pady=4)
    make_btn(btn_frame, "   Choose Another Level", choose_level, bg="#1e2d50", hover="#2d4070").pack(pady=4)
    make_btn(btn_frame, "✕   Exit",              exit_game,    bg="#450a0a", hover="#7f1d1d").pack(pady=4)


# ── Main game loop ────────────────────────────────────────────────────────────

def main():
    level_index = int(sys.argv[1])

    window = turtle.Screen()
    window.bgcolor("#050816")
    window.title("Escape the Maze")
    window.setup(width=700, height=700)

    pen            = Pen()
    player         = Player()
    endpoint_turtle = EndPoint()

    level = levels[level_index]

    # Draw everything at once (faster, no tile-by-tile animation)
    window.tracer(0)
    level.draw(pen, player, endpoint_turtle)
    window.update()
    window.tracer(1)

    win_shown = [False]   # mutable flag so closures can reset it

    def check_win():
        if win_shown[0] or level.endpoint is None:
            return
        px = round(player.xcor())
        py = round(player.ycor())
        ex, ey = level.endpoint
        if px == ex and py == ey:
            win_shown[0] = True
            show_win_popup(window, pen, player, endpoint_turtle,
                           level, level_index, win_shown)

    def move(action):
        action()
        check_win()

    window.listen()
    window.onkey(lambda: move(lambda: player.go_up(level.walls)),    "Up")
    window.onkey(lambda: move(lambda: player.go_down(level.walls)),  "Down")
    window.onkey(lambda: move(lambda: player.go_left(level.walls)),  "Left")
    window.onkey(lambda: move(lambda: player.go_right(level.walls)), "Right")

    turtle.done()


if __name__ == "__main__":
    main()