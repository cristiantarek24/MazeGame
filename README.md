# 🌀 Escape the Maze

A Python-based maze game featuring manual navigation and AI-powered pathfinding using **BFS**, **DFS**, and **A\*** algorithms — built with `turtle`, `tkinter`, and `pygame`.

---

## 📸 Preview

```
XXXXXXXXXXXXXXXXXXXXXXXXX
XP  X    X              X
X  X    X               X
...
X                     E X
XXXXXXXXXXXXXXXXXXXXXXXXX
```

> `P` = Player Start &nbsp;|&nbsp; `E` = Exit &nbsp;|&nbsp; `X` = Wall

---

## 🎮 Features

- 🗺️ **3 handcrafted maze levels** with increasing difficulty
- 🧠 **AI Solver** — watch BFS, DFS, or A\* solve the maze step by step
- 🎵 **Background music** that loops during gameplay
- 👣 **Step sound effects** triggered on every valid move
- 🏆 **Win sound** plays when the player reaches the exit
- 🪟 **Level select menu** with a clean dark-themed UI
- 🔄 **Play Again / Choose Level / Exit** from the win screen

---

## 🧠 Algorithms

| Algorithm | Strategy | Shortest Path? |
|-----------|----------|----------------|
| **BFS** | Explores level by level using a queue | ✅ Yes |
| **DFS** | Explores deep along each branch first | ❌ No |
| **A\*** | Uses cost + heuristic (Manhattan distance) | ✅ Yes |

---

## 📁 Project Structure

```
escape-the-maze/
│
├── Menu.py               # Level select screen (tkinter)
├── run_game.py           # Main game loop (turtle + tkinter)
├── Maze.py               # Level grids, Player, Pen, EndPoint classes
├── search_algorithms.py  # BFS, DFS, A* implementations
│
├── Block.gif             # Wall tile sprite
├── door.gif              # Exit sprite
├── elf_side01_idle.gif   # Player sprite (facing right)
├── elf_side02_idle.gif   # Player sprite (facing left)
│
├── background.mp3        # Background music (looping)
├── step.wav              # Footstep sound effect
└── win.wav               # Victory sound effect
```

---

## ⚙️ Requirements

- Python 3.8+
- `pygame`

Install dependencies:

```bash
pip install pygame
```

> `turtle` and `tkinter` are included in Python's standard library.

---

## 🚀 How to Run

```bash
python Menu.py
```

1. The level select menu will appear
2. Choose a level (1, 2, or 3)
3. Use **arrow keys** to navigate manually
4. Or click **BFS / DFS / A\*** to watch the AI solve it

---

## 🕹️ Controls

| Key | Action |
|-----|--------|
| `↑` `↓` `←` `→` | Move player |
| `BFS` button | Solve with Breadth-First Search |
| `DFS` button | Solve with Depth-First Search |
| `A*` button | Solve with A\* Search |

---

## 🗺️ Level Design

Levels are defined as grids of characters in `Maze.py`:

| Character | Meaning |
|-----------|---------|
| `X` | Wall |
| `P` | Player start position |
| `E` | Exit (goal) |
| ` ` | Open path |

Adding a new level is as simple as appending a new `Level([...])` to the `levels` list.

---

## 📚 Concepts Demonstrated

- Graph traversal algorithms (BFS, DFS, A\*)
- Heuristic search and Manhattan distance
- GUI programming with `tkinter` and `turtle`
- Audio management with `pygame.mixer`
- Multi-process architecture (Menu → Game subprocess)

---

## 👥 Authors

| Name |
|------|
| Cristian Tarek |
| Shahd Elmallah |
| Hanin Hani |
| Rahma Adel |
| Sabry Amir |

**Faculty of Computers and Information**

---

## 📄 License

This project is for educational purposes.
