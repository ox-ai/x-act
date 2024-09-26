




bash_script = """
#!/bin/bash
echo "Updating system..."
echo "$SUDO_PASS" | sudo -S apt update
echo "$SUDO_PASS" | sudo -S apt upgrade -y
echo "Cleaning up..."
echo "$SUDO_PASS" | sudo -S apt autoremove -y
echo "$SUDO_PASS" | sudo -S apt clean
echo "System maintenance completed!"
"""


sudo apt-get install xdotool
