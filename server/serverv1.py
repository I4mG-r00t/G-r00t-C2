from flask import Flask, request, jsonify

app = Flask(__name__)
port = 4444
lhost = '0.0.0.0'

# Endpoint to send commands to the agent
@app.route('/command', methods=['GET'])
def send_command():
    # Example command to run on the agent
    command = "whoami"  
    return jsonify({"command": command})

# Run the server
if __name__ == '__main__':
    app.run(lhost, port)