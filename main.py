import tkinter as tk
import subprocess
import sys
import os




# Tkinter level-select menu shown before the game starts
class Menu:
    # Color palette for the dark UI theme
    BG = "#0b1020"
    PANEL_BG = "#121a33"
    BUTTON_BG = "#1f2a4d"
    BUTTON_HOVER = "#2f3f73"
    BUTTON_TEXT = "#ffffff"
    ACCENT = "#7c5cff"
    ACCENT_2 = "#2dd4bf"

    def __init__(self):
        self.root = tk.Tk()
        self._setup_window()
        self._build_ui()

    # Centers the window on screen using screen dimensions at runtime
    def _setup_window(self):
        self.root.title("Escape the Maze")
        self.root.configure(bg=self.BG)
        self.root.resizable(False, False)
        self.root.update_idletasks()
        w, h = 420, 520
        x = (self.root.winfo_screenwidth() - w) // 2
        y = (self.root.winfo_screenheight() - h) // 2
        self.root.geometry(f"{w}x{h}+{x}+{y}")

    # Builds the card layout: title, divider, level buttons, footer tip
    def _build_ui(self):
        container = tk.Frame(self.root, bg=self.BG)
        container.pack(fill="both", expand=True, padx=20, pady=20)

        card = tk.Frame(
            container,
            bg=self.PANEL_BG,
            highlightthickness=2,
            highlightbackground=self.ACCENT,
            bd=0,
        )
        card.place(relx=0.5, rely=0.5, anchor="center", width=360, height=460)

        # Title
        tk.Label(
            card,
            text="ESCAPE\nTHE MAZE",
            font=("Arial", 24, "bold"),
            fg="white",
            bg=self.PANEL_BG,
            justify="center",
        ).pack(pady=(30, 10))

        # Subtitle
        tk.Label(
            card,
            text="Choose your challenge",
            font=("Arial", 12),
            fg="#cbd5e1",
            bg=self.PANEL_BG,
        ).pack(pady=(0, 20))

        # Two-tone accent divider
        glow = tk.Canvas(card, width=280, height=4, bg=self.PANEL_BG, highlightthickness=0)
        glow.pack()
        glow.create_rectangle(0, 0, 140, 4, fill=self.ACCENT, outline=self.ACCENT)
        glow.create_rectangle(140, 0, 280, 4, fill=self.ACCENT_2, outline=self.ACCENT_2)

        # Level buttons
        button_frame = tk.Frame(card, bg=self.PANEL_BG)
        button_frame.pack(pady=30)

        for i, label in enumerate(("Level 1", "Level 2", "Level 3")):
            btn = tk.Button(
                button_frame,
                text=label,
                command=lambda idx=i: self._start_level(idx),
            )
            self._style_button(btn)
            btn.pack(fill="x", pady=8)

        # Footer hint
        tk.Label(
            card,
            text="Tip: Pick a harder level for a bigger maze!",
            font=("Arial", 10, "italic"),
            fg="#94a3b8",
            bg=self.PANEL_BG,
        ).pack(side="bottom", pady=18)

    # Applies the dark theme and hover effect to a button
    def _style_button(self, button):
        button.configure(
            bg=self.BUTTON_BG,
            fg=self.BUTTON_TEXT,
            activebackground=self.BUTTON_HOVER,
            activeforeground=self.BUTTON_TEXT,
            relief="flat",
            bd=0,
            highlightthickness=0,
            padx=20,
            pady=12,
            cursor="hand2",
            font=("Arial", 14, "bold"),
        )
        button.bind("<Enter>", lambda _: button.configure(bg=self.BUTTON_HOVER))
        button.bind("<Leave>", lambda _: button.configure(bg=self.BUTTON_BG))

    # Destroys the menu and launches the selected level in a separate process
    def _start_level(self, level_index):
        self.root.withdraw()
        from Maze import levels
        script_dir = os.path.dirname(os.path.abspath(__file__))
        proc = subprocess.Popen([
            sys.executable,
            os.path.join(script_dir, "run_game.py"),
            str(level_index)
        ])
        self._wait_for_game(proc)

    def _wait_for_game(self, proc):
        if proc.poll() is None:
            self.root.after(200, lambda: self._wait_for_game(proc))
        elif proc.returncode == 2:
            self.root.deiconify()
        else:
            self.root.destroy()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    Menu().run()