import sys
import time
import requests

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
            # Here you can add logic to execute the command if needed
        else:
            print("No command received or an error occurred.")
        
        # Wait 10 seconds before the next check-in
        time.sleep(10)

if __name__ == "__main__":
    main()
