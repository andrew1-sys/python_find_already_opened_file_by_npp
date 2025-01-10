import os
import sys
import pygetwindow as gw
import pyautogui
import time
import subprocess
import ctypes

# Constants
NOTEPADPP_PATH = r"C:\\Program Files (x86)\\Notepad++\\notepad++.exe"
ACTIVATION_RETRIES = 3  # Number of retries to activate a window
PAUSE_DURATION = 0.05  # Pause duration between retries

def get_notepad_windows():
    """Get all active Notepad++ windows."""
    return gw.getWindowsWithTitle("Notepad++")

def bring_window_to_front(window, retries=ACTIVATION_RETRIES):
    """Bring the Notepad++ window to the front, retrying if necessary."""
    for attempt in range(retries):
        if window.isMinimized:
            window.restore()  # Restore the window if it is minimized
        window.activate()
        time.sleep(PAUSE_DURATION)
        if gw.getActiveWindow() == window:  # Verify if the window is active
            return True
        print(f"Attempt {attempt + 1} to activate the window failed. Retrying...")
    return False

def check_if_file_opened_in_active_tab(file_name):
    """Check if the file is opened in the active tab of the current Notepad++ window."""
    active_window = gw.getActiveWindow()
    return file_name.lower() in active_window.title.lower()

def switch_to_previous_tab():
    """Switch to the previous tab (Ctrl + PgUp)."""
    pyautogui.hotkey('ctrl', 'pgup')
    time.sleep(PAUSE_DURATION)

def search_tabs_for_file(file_name, window):
    """Search for the file among the tabs of the current Notepad++ window."""
    tab_titles = set()  # Store unique tab names

    for _ in range(20):  # Limit to a maximum of 20 tab switches
        active_window = gw.getActiveWindow()  # Get the current active window

        if active_window.title in tab_titles:
            break  # Stop search if the tab title repeats

        tab_titles.add(active_window.title)  # Add the tab title to the set

        if check_if_file_opened_in_active_tab(file_name):
            return True

        switch_to_previous_tab()  # Move to the previous tab
    return False

def find_and_focus_file(file_name):
    """Iterate over all windows and tabs to find the desired file."""
    notepad_windows = get_notepad_windows()

    # Iterate through all windows
    for window in notepad_windows:
        if bring_window_to_front(window):  # Check if the window activation is successful
            # Try to find the file in the current window's tabs
            if search_tabs_for_file(file_name, window):
                return window

    return None

def get_long_path(short_path):
    """Converts a short path to a long path using Windows API."""
    buffer = ctypes.create_unicode_buffer(260)  # MAX_PATH is 260
    ctypes.windll.kernel32.GetLongPathNameW(short_path, buffer, 260)
    return buffer.value or short_path  # Return original if conversion fails

def search_file_in_processes(file_name):
    """Search for the file in the titles of all Notepad++ processes."""
    
    # Спочатку конвертуємо короткий шлях в довгий
    long_file_name = get_long_path(file_name)
    
    print(f"Searching for file: {long_file_name}")
    
    notepad_windows = get_notepad_windows()
    for window in notepad_windows:
        print(f"Checking window title: {window.title}")
        # Порівнюємо з довгим шляхом, не зважаючи на регістр
        if long_file_name.lower() in window.title.lower():
            print(f"File found in window: {window.title}")
            return window
    
    print("File not found in any window.")
    #input("Press Enter ..")
    return None


def open_file_in_new_instance(file_path):
    """Open the file in a new instance of Notepad++ with -multiInst -nosession flags."""
    print(f"Launching a new Notepad++ instance to open file {file_path} with -multiInst -nosession flags.")
    subprocess.Popen([NOTEPADPP_PATH, "-multiInst", "-nosession", file_path])  # Use Popen for asynchronous launch
    time.sleep(PAUSE_DURATION)

if __name__ == "__main__":
    # Check if the file path is provided via command line
    if len(sys.argv) < 3:
        print("Usage: python script.py <mode> <file_path>")
        print("Mode: 1 - Full search, 0 - Search only in processes")
        sys.exit(1)

    search_mode = int(sys.argv[1])
    file_to_find = sys.argv[2]

    if search_mode == 1:
        # First, search all windows for the file
        print(f"Checking if the file {file_to_find} is open in existing Notepad++ windows.")
        window = find_and_focus_file(file_to_find)
    else:
        # Quick search: search only in process titles
        print(f"Quick search mode: Checking if the file {file_to_find} is open in Notepad++ process titles.")
        window = search_file_in_processes(file_to_find)

    if window:
        # If the file is found, activate it
        print(f"File {file_to_find} found and activated.")
        bring_window_to_front(window)
    else:
        # If the file is not found, open it in a new instance
        print(f"File {file_to_find} not found. Opening a new instance.")
        open_file_in_new_instance(file_to_find)

    # Exit the program
    sys.exit(0)
