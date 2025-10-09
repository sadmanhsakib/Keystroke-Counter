from pynput import keyboard, mouse
import datetime
import os
import threading
import time

day_count = 0
last_logging_date = ""
keystroke_count = 0
click_count = 0
lines = []

# creating a log file if it doesn't exist
if not os.path.exists("log.csv"):
    today = datetime.datetime.now().date()
    
    with open("log.csv", 'w') as file:
        # writing the initial lines
        file.write("No,Date,Keystroke-Count,Click-Count\n")
        file.write(f"1,{today},0,0")

log_file = "log.csv"

def main():
    global day_count, last_logging_date, keystroke_count, click_count, lines
    
    # getting the data from the last line
    with open(log_file, 'r') as file:
        lines = file.readlines()
        
        parts = lines[-1].split(',')
        day_count = int(parts[0])
        last_logging_date = parts[1] 
        keystroke_count = int(parts[2])
        click_count = int(parts[3])
    
    log()

    # threads are used to allow both listeners to run concurrently
    # using the daemon=True argument to ensure they close when the main program exits
    keyboard_thread = threading.Thread(target=keyboard_listener, daemon=True)
    mouse_thread = threading.Thread(target=mouse_listener, daemon=True)
    
    # starting the listener threads
    keyboard_thread.start()
    mouse_thread.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting...")


# counts every any key is pressed except Fn
def on_key_press():
    global keystroke_count
    keystroke_count += 1


# counts specified mouse button clicks
def on_click(x, y, button, pressed):
    global click_count

    if pressed:
        # only counts left, right and middle clicks
        if button == mouse.Button.left or button == mouse.Button.right or button == mouse.Button.middle:
            click_count += 1
        

# logs the counts every 60 seconds
def log():
    global keystroke_count, click_count, last_logging_date, day_count, lines
    
    today_date = datetime.datetime.now().date().strftime("%Y-%m-%d")

    # if the date has changed, log the counts and reset other values
    if last_logging_date != today_date:
        day_count += 1
        keystroke_count = 0
        click_count = 0
    else:
        lines.pop(-1)
    
    lines.append(f"{day_count},{today_date},{keystroke_count},{click_count}\n")
    
    # writes the data to the log file
    with open(log_file, 'w') as file:        
        file.writelines(lines)
        
    # schedule the next log check in 5 seconds
    threading.Timer(5, log).start()

def keyboard_listener():
    # listens to the keyboard input after logging in, no matter where the focus is
    with keyboard.Listener(on_press=on_key_press) as listener:
        listener.join()
        
def mouse_listener():
    # listens to the mouse clicks after logging in, no matter where the focus is
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()
        
if __name__ == "__main__":
    main()