# radus-cg100-applications

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
