from pynput import keyboard, mouse
from database import db
import config
import datetime, os
import threading
import asyncio, pytz

cache_file = "cache.txt"

# getting the date minding the timezone
timezone = pytz.timezone(config.TIMEZONE)
today = datetime.datetime.now(timezone).strftime("%Y-%m-%d")

# creating the cache file if it doesn't exist
if not os.path.exists(cache_file):
    with open(cache_file, "w") as file:
        file.write(f"{today},0,0,0.00")


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
    # getting the last data from the cache file
    with open(cache_file, "r") as file:
        lines = file.readlines()
        parts = lines[-1].split(",")

        tracker.keystroke_count = int(parts[1])
        tracker.click_count = int(parts[2])

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
        if (
            button == mouse.Button.left
            or button == mouse.Button.right
            or button == mouse.Button.middle
        ):
            tracker.click_count += 1


# runs the log function periodically
async def periodic_log():
    while True:
        # log_activity() function is called every 10 seconds
        await asyncio.sleep(2)
        await log_activity()


async def log_activity():
    if tracker._logging:
        return

    tracker._logging = True
    keystroke_count, click_count = tracker.get_counts()

    try:
        ratio = round(keystroke_count / click_count, 2)
    except ZeroDivisionError:
        ratio = 0.00

    with open("cache.txt", "r") as file:
        line = file.readline()
        last_log_date = line.split(",")[0]

    if last_log_date != today:
        # inserting the log data into the database
        await db.connect()
        await db.set_log(today, keystroke_count, click_count, ratio)

        # resetting the counts
        tracker.reset_counts()

    # updating the cache file with the latest counts
    with open(cache_file, "w") as file:
        file.write(f"{today},{keystroke_count},{click_count},{ratio}")

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
