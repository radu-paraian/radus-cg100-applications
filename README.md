# Radu's CG100 Applications

Simple games for the CASIO fx-CG100 graphing calculator, written in its Python app (MicroPython 1.9.4). Each game is a single `.py` file with no dependencies.

## Games

### Snake (`snake.py`)

Classic Snake with a checkered green board, a blue snake with googly eyes, and apples to eat. It keeps your best score for as long as the script runs.

| Key | Action |
| --- | --- |
| Arrows | Steer (the snake starts moving on your first arrow press) |
| Left / Right on the menu card | Change speed (1 to 9) |
| OK | Start a game, or pause and resume |
| AC | Quit |

### 2048 (`g2048.py`)

The classic sliding-tile puzzle: merge matching numbers to reach 2048. Tiles slide smoothly and new tiles pop in. It keeps your best score for as long as the script runs.

| Key | Action |
| --- | --- |
| Arrows | Slide the tiles |
| OK | New game (press OK again to confirm) |
| Any other key | Turn the slide animation on or off |
| AC | Quit |

The file is called `g2048.py` because Python module names can't start with a digit, and the calculator imports a script when it runs it.

## Installing a game

1. Plug the calculator into your computer with a USB data cable. Press **AC** first if a script is running, so the connection prompt appears.
2. On the calculator, choose **[USB Flash]** and press **OK**.
3. Copy the `.py` file into the root of the Calculator Drive that shows up on your computer.
4. Eject the drive and wait for **Complete!** on the calculator, then press **OK**.
5. Open **HOME > Python > File > Open**, pick the file, and run it.

You can also download each game from the [Releases](https://github.com/radu-paraian/radus-cg100-applications/releases) page.

## Development

The calculator's Python rules (allowed modules, file limits, screen and key details) are in [AGENTS.md](AGENTS.md).

## License

Apache 2.0. See [LICENSE](LICENSE).
