import tkinter as tk
from PIL import Image, ImageTk
import pyscreenshot as ImageGrab
import cv2
import numpy as np
import argparse
import time

# Variables to store the initial click position
start_x = 0
start_y = 0
screenshot = None

# Function to capture the screen and apply a blur effect
def capture_and_blur(event=None):
    global start_x, start_y, screenshot, root

    # Capture the entire screen
    if not screenshot:
        screenshot = ImageGrab.grab()

    ## Get the window's coordinates and dimensions
    x = root.winfo_x()
    y = root.winfo_y()
    width = root.winfo_width()
    height = root.winfo_height()
 
    start_x = x
    start_y = y

    w, h = screenshot.size

    #if the window goes off the edge of the screen.
    end_x = (start_x + width)
    if end_x > w :
        end_x= w
    end_y = (start_y + height)
    if end_y > h:
        end_y = h

    #FIXME: would be more memory efficient to crop here, but it doesn't work
    #window = screenshot.crop((x, y, x+600, y+300))
    #screenshot.crop((start_x, start_y, start_x+w, start_y+h))
    #Crop the image
    #print(f'x: {x} y: {y} width:{width} height: {height}')
    #window.show()

    # Convert the screenshot to a NumPy array
    screenshot_np = np.array(screenshot)
    cropped_screenshot = screenshot_np[y:y+height, x:x+width]#= screenshot_np[y:y+height, x:x+width]

    # Apply a blur effect using OpenCV
    blurred_screenshot = cv2.GaussianBlur(cropped_screenshot, (0, 0), sigmaX=5)

    # Convert the blurred image to a format that Tkinter can display
    blurred_image = Image.fromarray(blurred_screenshot)
    blurred_image = ImageTk.PhotoImage(blurred_image)

    # Update the Tkinter label to display the blurred image
    label.config(image=blurred_image)
    label.image = blurred_image

# Function to handle the mouse button press event
def on_mouse_press(event):
    global start_x, start_y
    if quick_kill_mode:
        quit()
        return
    start_x = event.x_root - root.winfo_x()
    start_y = event.y_root - root.winfo_y()

# Function to handle the mouse motion event for dragging
def on_mouse_drag(event):
    x = event.x_root - start_x
    y = event.y_root - start_y
    root.geometry('+{}+{}'.format(x, y))

# Function to handle the mouse button release event
def on_mouse_release(event):
    x = event.x_root - start_x
    y = event.y_root - start_y
    root.geometry('+{}+{}'.format(x, y))
    capture_and_blur()  # Update the blurred image at the new coordinates

def do_popup(event):
    try:
        menu.tk_popup(event.x_root, event.y_root)
    finally:
        menu.grab_release()

def quit():
    global root
    root.destroy()

def reload_image():
    global root, screenshot
    screenshot = None
    width = root.winfo_width()
    height = root.winfo_height()
    root.destroy()
    screenshot = ImageGrab.grab()
    create_window((width,height,start_x,start_y))

def create_window(window_dim):
    global root, menu, label
    w,h,x,y = window_dim
    # Create a Tkinter window with no decorations and set the size to 600x300
    root = tk.Tk()
    root.overrideredirect(True)
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))

    # Create a label to display the blurred screenshot
    label = tk.Label(root)
    label.pack(fill=tk.BOTH, expand=True)

    # Capture and blur the screen initially
    capture_and_blur()

    # Bind mouse events to the root window
    root.bind('<ButtonPress-1>', on_mouse_press)
    root.bind('<B1-Motion>', on_mouse_drag)
    root.bind('<ButtonRelease-1>', on_mouse_release)

    # Create a context menu to capture a new image
    menu = tk.Menu(root, tearoff=0)
    menu.add_command(label="Reload (insecure!)", command=reload_image, state="normal")
    menu.add_separator()
    menu.add_command(label="Quit", command=quit, state="normal")
    label.bind("<Button-3>", do_popup)

    # Set an interval for updating the blurred image (e.g., every 1 second)
    root.after(1000, capture_and_blur)

    # Start the Tkinter main loop
    root.mainloop()

def main():
    global quick_kill_mode
    # Parse the command line
    parser = argparse.ArgumentParser(
                prog='blur_box',
                description='A *simple* blurred window to hide URIs while screencasting.  Note the blurred screen does not update, when using "Reload" the screen is displayed momentarily',
                epilog='\nexample usage:\n \n> python blur_box.py --x 10 --y 20 --width 500 --height 100\n Creates a blur box at x=10, y=20, of size 500x100')
    parser.add_argument("--x", type=int, default=10, help="X coordinate (default: 0)")
    parser.add_argument("--y", type=int, default=10, help="Y coordinate (default: 0)")
    parser.add_argument("--width", type=int, default=500, help="Width (default: 500)")
    parser.add_argument("--height", type=int, default=80, help="Height (default: 80)")
    parser.add_argument("-k", action="store_true", help="Quick kill mode - (window closes on click)")
    args = parser.parse_args()
    quick_kill_mode = args.k
    # Create the blurry window
    create_window((args.width, args.height, args.x, args.y))

if __name__ == "__main__":
    main()