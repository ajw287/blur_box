# blur_box
A *simple* blurred window to hide URIs while screencasting. Note the blurred
screen does not update, when using "Reload" the screen is displayed
momentarily
```
options:
  -h, --help       show this help message and exit
  --x X            X coordinate (default: 0)
  --y Y            Y coordinate (default: 0)
  --width WIDTH    Width (default: 500)
  --height HEIGHT  Height (default: 80)
  -k               Quick kill mode - (window closes on click)
```
example usage:

```python blur_box.py --x 10 --y 20 --width 500 --height 100```

Creates a blur box at x=10, y=20, of size 500x100
