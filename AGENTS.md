# CASIO fx-CG100 Python Rules

Every `.py` file in this project runs on the CASIO fx-CG100 / fx-1AU GRAPH Python app.
Source: https://support.casio.com/global/en/calc/manual/fx-CG100_1AUGRAPH_en/BONDSYlkjdoxxc.html
These rules are mandatory. If a script breaks one, it is broken.

## Runtime
- **MicroPython 1.9.4**, adapted for CASIO. This is not desktop CPython, and the app supports only part of MicroPython.
- Use only these modules (they are all the Catalog lists): **built-ins, `math`, `random`, `matplotlib.pyplot`, `turtle`, `casioplot`**. Other imports (`os`, `sys`, `time`, `numpy`, `typing`, `dataclasses`, etc.) may not exist. A command the calculator doesn't support raises an error when the script runs.
- These come from MicroPython 1.9.4 itself, not from the manual: no f-strings (use `str()`, `+` or `%`), no walrus `:=`, no type hints, no `async`. Keep the syntax to plain Python 3.4-era code.
- Results can differ from the calculator's other apps, because MicroPython does the math.
- Memory is small. Keep data small, avoid large lists or strings, and expect `Memory ERROR`.

## File format (hard limits)
- **ASCII only**, in code, strings and comments. Allowed: `A-Z a-z 0-9` and ``! " # $ % & ' ( ) * + , - . / : ; < = > ? @ [ \ ] ^ _ ` { | } ~`` plus space. No unicode quotes, accents, emoji or `π` (write `pi`).
- **No more than 300 lines per file and no more than 255 characters per line.** A longer file can't be shown or edited on the calculator. It can only be loaded with `from name import *`.
- **Indent with 2 spaces**, the calculator's auto-indent. No tabs (the calculator turns each tab into 2 spaces).
- Newlines: the calculator saves CR+LF, and LF works too.
- Encoding: UTF-8 or ASCII, with ASCII content only.

## File names
- Use ASCII characters only, and none of `\ / : * ? " < > | .` before `.py`.
- **Keep names to 8 characters or fewer** (plus `.py`). Longer names are shown shortened (`AAAABBBBCC.py` becomes `AAAABB~1.py`), which breaks `import`.
- In Exam Mode, names can be **at most 5 characters, lowercase letters and digits only**. Prefer names like this anyway so scripts work in every mode.
- `module.py` is the default file the app opens. Don't use that name for project files.

## Running and output
- Running a file imports it into Shell. Top-level code runs, and globals and functions stay available in Shell.
- A bare expression only echoes in Shell. Inside a file, wrap it in `print(...)`, e.g. `print(axis())` or `print(pencolor())`.
- Shell input is limited to 255 characters, and an output line to 509. History keeps 200 lines.
- Pressing AC stops a running script. Infinite loops (`while True:`) are acceptable for interactive programs.

## casioplot (pixel drawing)
- Screen is **384x192**. `x` runs 0..383 and `y` runs 0..191, origin at the **top-left**, coordinates **int only**.
- `set_pixel(x,y[,color])`, `get_pixel(x,y)` returns an RGB tuple or nothing if off-screen, `clear_screen()`, `show_screen()`, `getkey()`.
- `draw_string(x,y,s[,color[,size]])`: `s` must be ASCII, and size is `"large"`, `"medium"` (default) or `"small"`.
- Color is an `(r,g,b)` tuple or list with values 0..255. The default is black `(0,0,0)`.
- Drawing off-screen is silently ignored: nothing is drawn and no error is raised.
- The screen only updates on `show_screen()` or when the script ends. It is cleared by `clear_screen()` or Shell initialization. Draw a whole frame, then call `show_screen()` once.
- `getkey()` key codes are `row*10 + column` from the top of the keypad (rows 1-9, columns 1-6). The D-pad is 14 up, 23 left, 25 right, 34 down, 24 center, and 16 and 26 are the tall key on the right. Rows 6-9 have 5 keys. Two keys return no code: the top-left key and row 6, column 5. **Check codes on the device before relying on them.**

## matplotlib.pyplot (CASIO proprietary subset)
- Import with `from matplotlib.pyplot import *` or `import matplotlib.pyplot`.
- Only these functions exist, with exactly these signatures:
  - `show()`, `axis([xmin,xmax,ymin,ymax])`, `axis("on"|"off"|"auto")`, `axis()`
  - `grid(option[,color])`, `grid(color)`, `grid()`
  - `plot(x,y[,color])`, `plot([listx,]listy[,color])`
  - `bar(x,y[,width])`, `bar(listx,listy[,width])` (width defaults to 0.8)
  - `scatter(x,y)`, `scatter(listx,listy)`
  - `hist(x|listx[,bins])` or `hist(x|listx,listbins)` (bins defaults to 10)
  - `arrow(x,y,dx,dy[,edgecolor[,facecolor[,head_width[,head_length]]]])`. Always pass the optional arguments by keyword.
  - `text(x,y,text)`
- Colors are `"b"/"blue" "r"/"red" "g"/"green" "m"/"magenta" "k"/"black" "c"/"cyan" "y"/"yellow" "w"/"white" "grey" "orange" "purple" "brown" "pink"`.
- `show()` resets the graphs, axis and grid. Only what was set up between the last two `show()` calls is drawn.
- Axes default to `[0,1,0,1]`. `plot`, `bar`, `scatter` and `hist` auto-scale the axes, but `arrow` and `text` don't, so call `axis([...])` yourself for those.
- The axis is always black, and `text` and points are always black and `+`-shaped. `axis("auto")` only works after a drawing call.
- When no color is given, colors cycle blue, red, green, magenta, black, cyan, yellow, and `show()` resets the cycle. `bar`, `scatter` and `hist` don't take a color argument.

## turtle (CASIO proprietary subset)
- Import with `from turtle import *` or `import turtle`.
- Coordinates are fixed: x runs **-192..191** and y **-95..96**, origin at the center.
- Only these functions exist:
  - Pen: `pendown()`, `penup()`, `pencolor(name|[r,g,b] 0..1)`, `pencolor()`, `pensize(n 0..5)`, `width(n)`
  - Move: `right(a)`, `left(a)`, `setheading(a)` (angles 0<=a<360, 0 is east, counter-clockwise), `forward(n)`, `backward(n)`
  - Position: `goto(x,y)`, `setposition(x,y)`, `setx(x)`, `sety(y)`, `home()`
  - Draw: `circle(radius[,extent])`, `write(text)`
  - Settings: `shape("classic"|"turtle")`, `speed(0..10 | "fastest","fast","normal","slow","slowest")` (0 is fastest), `showturtle()`, `hideturtle()`
  - Queries: `isvisible()`, `isdown()`, `xcor()`, `ycor()`, `position()`, `distance(x,y)`, `towards(x,y)`, `heading()`
  - Reset: `reset()`, `clear()`
- Pen color names are black, blue, green, red, cyan, yellow, magenta, white, orange, purple, brown, pink and grey. RGB values are **0..1 floats**, unlike casioplot's 0..255.
- The default state is (0,0), heading 0, black pen, pen down, width 1, speed 5, turtle shown, shape "classic".

## Project conventions
- Write one self-contained script per program. A script may import its own project files, but globals from imported files don't show in the Variable (V) menu.
- Before saying a script is finished, check that it is ASCII only, has at most 300 lines and 255 characters per line, uses 2-space indents, has an 8-character or shorter file name, and imports only allowed modules.
