import subprocess
import time
import pyautogui
import pygetwindow as gw

# Function to open Google Chrome
def open_chrome():
    # Adjust the path to Chrome executable as needed

    subprocess.Popen(["google-chrome"])
    time.sleep(5)  # Wait for Chrome to open

# Function to perform the search
def search_query(query):
    # Get the Chrome window
    chrome_window = None
    while chrome_window is None:
        try:
            chrome_window = gw.getWindowsWithTitle('Google Chrome')[0]
        except IndexError:
            time.sleep(1)

    # Bring the Chrome window to the foreground
    chrome_window.activate()

    # Open a new tab
    pyautogui.hotkey('ctrl', 't')
    time.sleep(1)

    # Type the search query
    pyautogui.typewrite('https://www.google.com\n', interval=0.1)
    time.sleep(2)  # Wait for Google to load

    pyautogui.typewrite(query, interval=0.1)
    pyautogui.press('enter')

# Main function
if __name__ == "__main__":
    open_chrome()
    search_query('what is ox')
