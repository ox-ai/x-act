import asyncio
import os
from xact.act.action.gui import ComputerTool, ToolError  # Assume saved as computer_tool_module.py
from xact.act.action import gui

gui.Action
async def main():
    # Set the required environment variables
    os.environ["WIDTH"] = "1280"  # Screen width in pixels
    os.environ["HEIGHT"] = "800"  # Screen height in pixels
    os.environ["DISPLAY_NUM"] = "0"  # Optional, for specifying the display number

    # Initialize the ComputerTool
    tool = ComputerTool()

    # Example 1: Type text
    try:
        print("Typing 'Hello, World!' on screen...")
        await tool(action="type", text="Hello, World!")
    except ToolError as e:
        print("Error during typing:", e)

    # Example 2: Move the mouse to a coordinate
    try:
        print("Moving mouse to coordinate (100, 200)...")
        await tool(action="mouse_move", coordinate=(100, 200))
    except ToolError as e:
        print("Error during mouse move:", e)

    # Example 3: Perform a left-click
    try:
        print("Performing left click...")
        await tool(action="left_click")
    except ToolError as e:
        print("Error during left click:", e)

    # Example 4: Take a screenshot
    try:
        print("Taking a screenshot...")
        screenshot_result = await tool(action="screenshot")
        print("Screenshot captured as base64 string:")
        print(screenshot_result.base64_image)
    except ToolError as e:
        print("Error during screenshot:", e)

# Run the main function
asyncio.run(main())
