from pynput import keyboard, mouse
from database import db
import datetime
import threading
import time
import asyncio

class ActiveListener:
    def __init__(self):
        self.keystroke_count = 0
        self.click_count = 0
        self._lock = threading.Lock()  # thread safety
        self._logging = False  # prevents multiple logging at the same time

    def increment_keystroke(self):
        with self._lock:
            self.keystroke_count += 1

    def increment_click(self):
        with self._lock:
            self.click_count += 1

    def get_counts(self):
        with self._lock:
            return self.keystroke_count, self.click_count

    def reset_counts(self):
        with self._lock:
            self.keystroke_count = 0
            self.click_count = 0

tracker = ActiveListener()            

async def main():
    # connecting to the database
    await db.connect()
    last_log = await db.get_last_log()

    if last_log:
        # getting the data from the last line
        tracker.keystroke_count = int(last_log["keystroke_count"])
        tracker.click_count = int(last_log["click_count"])
    else:
        tracker.keystroke_count = 0
        tracker.click_count = 0
    
    # threads are used to allow both listeners to run concurrently
    # using the daemon=True argument to ensure they close when the main program exits
    keyboard_thread = threading.Thread(target=keyboard_listener, daemon=True)
    mouse_thread = threading.Thread(target=mouse_listener, daemon=True)

    # starting the listener threads
    keyboard_thread.start()
    mouse_thread.start()

    asyncio.create_task(periodic_log())

    # keeps the program running 
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("Exiting...")


# counts every any key is pressed except Fn
def on_key_press():
    tracker.keystroke_count += 1


# counts specified mouse button clicks
def on_click(x, y, button, pressed):
    if pressed:
        # only counts left, right and middle clicks
        if button == mouse.Button.left or button == mouse.Button.right or button == mouse.Button.middle:
            tracker.click_count += 1


# runs the log function periodically
async def periodic_log():
    while True:    
        # log_activity() function is called every 10 seconds
        await asyncio.sleep(10)
        await log_activity()

async def log_activity():
    if tracker._logging:
        return
    
    tracker._logging = True
    keystroke_count, click_count = tracker.get_counts()
    
    try:
        ratio = round(keystroke_count/click_count, 2)
    except ZeroDivisionError:
        ratio = 0.00

    await db.set_log(keystroke_count, click_count, ratio)

    tracker._logging = False


def keyboard_listener():
    # listens to the keyboard input after logging in, no matter where the focus is
    with keyboard.Listener(on_press=on_key_press) as listener:
        listener.join()


def mouse_listener():
    # listens to the mouse clicks after logging in, no matter where the focus is
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()


if __name__ == "__main__":
    asyncio.run(main())
