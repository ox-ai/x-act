






import asyncio

from xact.act.action import bash

# Create an instance of BashTool
bash_tool = bash.BashTool()

async def main():
    # Start the BashTool session and run a cmd
    print("Starting BashTool and running the 'echo' cmd:")
    result = await bash_tool(cmd="echo Hello, BashTool!")
    print("Output:", result.output)  # Should display 'Hello, BashTool!'
    print("Error:", result.error)  # Should be empty if there's no error

    # Run another cmd in the same session
    print("\nRunning 'ls' cmd to list files in the current directory:")
    result = await bash_tool(cmd="ls")
    print("Output:", result.output)
    print("Error:", result.error)

    # Restart the BashTool session and run a cmd in the new session
    print("\nRestarting BashTool session and running 'pwd' cmd:")
    result = await bash_tool(cmd="bash",restart=True,)
    print("Output:", result.output)
    print("Error:", result.error)

# Run the async main function

import nest_asyncio
nest_asyncio.apply()

# Now you can use asyncio.run() in this environment
asyncio.run(main())

