import os
import signal
import subprocess


class xshell:
    def __init__(self) -> None:
        self.process = None
        self.pid = None
        self.end_list = []

    def start(self, code: list):
        # Start a program and get its process ID
        self.process = subprocess.Popen(
            code,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
        )
        self.pid = self.process.pid
        print(f"Process ID: {self.process.pid}")
        return self.process

    def commune(self, code):
        try:
            output, error = self.process.communicate(input=code)
        except Exception as e:
            print(f"Error: {e} \n{error}")

        return output

    def get_out(self, end_list=None):

        end_list = end_list or self.end_list
        output = ""
        loop = ""
        res = ""
        while True:

            output = self.process.stdout.readline()
            print("out : ",output, end="")  # Output received from the shell
            res +=output
            for e in self.end_list:
                if e in output:
                    loop = "break"
                    break

            if loop == "break":
                break
        return res

    def run(code: list):
        # Execute the script
        result = subprocess.run(code, capture_output=True, text=True)

        # Print the output
        print(result.stdout)

        return result.stdout

    def send(self, cmd, end_list=None):
        end_list = end_list or self.end_list
        try:
            # Send initial commands to the shell
            cmd_string = f"{cmd}\n"
            print(cmd)
            self.process.stdin.write(cmd_string)
            self.process.stdin.flush()

            return self.get_out(end_list)

        except Exception as e:
            print(f"Error: {e}")

        # finally:
        #     process.send_signal(signal.SIGINT) # Exit the shell
        #     process.stdin.flush()
        #     process.terminate()

    def kill(self, pid=None):
        pid = pid or self.process.pid

        # self.process.send_signal(signal.SIGINT) # Exit the shell
        # self.process.stdin.flush()
        # self.process.terminate()
        # self.process.kill()
        try:
            # Send the SIGTERM signal to terminate the process gracefully
            os.kill(pid, signal.SIGTERM)
            print(f"Process {pid} terminated.")
        except ProcessLookupError:
            print(f"Process {pid} not found.")
        except PermissionError:
            print(f"Permission denied to terminate process {pid}.")
        except Exception as e:
            print(f"An error occurred: {e}")
