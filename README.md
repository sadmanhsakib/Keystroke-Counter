> **⚠️ ARCHIVED PROJECT**  
> This project is archived and now part of my [Automation-Toolbox](https://github.com/sadmanhsakib/Automation-Toolbox) repository.

# KeyMouseStats

**KeyMouseStats** is a lightweight, background utility designed to track and log your daily keystrokes and mouse clicks. Built with performance and resilience in mind, it silently monitors input activity and persists daily statistics to a PostgreSQL database for long-term analysis.

## 🚀 Key Features

*   **Resilient Tracking:** Uses a local cache (`cache.txt`) to ensure data is never lost, even if the script crashes or the system restarts unexpectedly.
*   **Non-Blocking Performance:** Leverages Python's `threading` for input listeners and `asyncio` for database operations, ensuring zero impact on system performance.
*   **Daily Analytics:** Automatically aggregates and logs daily totals (Keystrokes, Clicks, and Ratio) to a PostgreSQL database.
*   **Background Operation:** Designed to run invisibly in the background.

## 💡 Real-World Use Cases

*   **Productivity Insights:** Correlate input volume with daily tasks to understand your peak productivity hours.
*   **Ergonomic Health:** Monitor usage intensity to help prevent Repetitive Strain Injury (RSI) by identifying days with excessive strain.
*   **Usage Statistics:** Satisfy curiosity about your daily interaction with your computer (e.g., for gamers or developers).

## 🛠️ Installation & Setup

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/sadmanhsakib/KeyMouseStats.git
    cd KeyMouseStats
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment**
    Create a `.env` file in the root directory:
    ```env
    DATABASE_URL=postgresql://user:password@localhost/dbname
    ```

4.  **Database Setup**
    Ensure you have a PostgreSQL database running. The script will automatically create the necessary schema and tables on the first run.

## 🏃 Usage

### Automatic Run (Startup)
To have this run automatically when you turn on your computer:

#### **Windows (Task Scheduler)**
For a more reliable startup experience than the Startup folder:
1.  Press `Win + R`, type `taskschd.msc`, and press Enter.
2.  In the right pane, click **Create Basic Task...**.
3.  **Name**: "KeyMouseStats" (or your preferred name). Click Next.
4.  **Trigger**: Select **When I log on**. Click Next.
5.  **Action**: Select **Start a program**. Click Next.
6.  **Program/script**: Browse and select your `pythonw.exe` (usually in your Python installation folder) or simply select the `main.pyw` file if `.pyw` is associated with Python correctly.
    *   *Tip*: To be safe, point to `pythonw.exe` and put the full path to `main.pyw` in the **Add arguments** box.
7.  Click **Finish**.

#### **macOS**
Add the script to your **Login Items** in System Settings or use `automator` to create an application that runs the script.

#### **Linux**
You can use the `autostart` directory.
1.  Create a `.desktop` file in `~/.config/autostart/` (e.g., `KeyMouseStats.desktop`).
2.  Add the following content (adjust paths as needed):
    ```ini
    [Desktop Entry]
    Type=Application
    Exec=/usr/bin/python3 /path/to/your/KeyMouseStats/main.pyw
    Hidden=false
    NoDisplay=false
    X-GNOME-Autostart-enabled=true
    Name=KeyMouseStats
    Comment=Start daily routine
    ```

## 📂 Project Structure

*   `main.pyw`: Core logic, initializes listeners and handles the main event loop.
*   `database.py`: Handles asynchronous PostgreSQL connections and table management.
*   `config.py`: Manages environment variables and configuration.
*   `cache.txt`: Local temporary storage for current day's stats.

## 🤝 Contributing

This project is solely developed and maintained by **[Sadman Sakib](https://github.com/sadmanhsakib)**.