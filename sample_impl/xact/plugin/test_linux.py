import subprocess
import time
import pyautogui
from xact.shell import xshell





# Function to perform the search
def search_query(query):
    # Use xdotool to focus Chrome window
    xshell.run(['xdotool', 'search', '--name', '"Google Chrome"', 'windowactivate'])
    time.sleep(1)

    # # Open a new tab
    # pyautogui.hotkey('ctrl', 't')
    # time.sleep(1)

    # Type the search query
    pyautogui.typewrite('https://www.google.com\n', interval=0.1)
    time.sleep(2)  # Wait for Google to load

    pyautogui.typewrite(query, interval=0.1)
    pyautogui.press('enter')
    time.sleep(2)




# Main function
if __name__ == "__main__":
    sh1 = xshell()
    sh1.start(["google-chrome"])
    time.sleep(5)  # Wait for Chrome to open
    search_query('what is ox-ai')
    print(sh1.process.pid)
    sh1.kill()
    sh1.process.kill()
    
