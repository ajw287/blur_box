# blur_box
<p align="center">
   <img src="./docs/images/blurred_username.png" alt="blurred screen image" width="300" title="blurred screen image">
</p>
A *simple* blurred window to hide URIs, usernames etc while recording video or screencasting. Note the blurred
screen does not update automatically, when using "Reload" the screen is displayed
momentarily.  'Blur box' can be dragged around or set to 'quick kill' mode.
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
