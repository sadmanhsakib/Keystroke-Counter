# Keystroke-Counter
This is a single Python script that reads the total number of keys and buttons pressed on the keyboard and mouse. It constantly reads user input and stores the number of buttons and keys pressed by the user. The script writes (creates, if the log.csv does not exist) data on a log.csv file.

<h3>How does it work?</h3>
At first, the script looks for a "log.csv" in its local directory. If there is no "log.csv" file, then it automatically creates one. After that, it keeps on reading user input and stores the data in the log.csv file. Another important thing is that the script doesn't store any data about the keys that were actually pressed or the buttons on the mouse that were actually pressed.

<h3>How to use?</h3>
0. Download & Install the pynput module with the help of the terminal using this command: "pip install pynput"<br> 
1. Clone the GitHub repository.<br>
2. Open the Task Scheduler. (If you are not using Windows, please follow the instructions for your operating system.)<br>
4. Create a new task for the script. (Trigger can be whatever the user wants. Personally, I set the trigger to "At log on".)<br>
