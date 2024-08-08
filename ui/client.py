import configparser
import socket
import time
import sys

config = configparser.ConfigParser()
config.read("config.ini")

host = str(config['AI']['local'])
port = int(config['AI']['port'])

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.connect((host, port))

        print("""Welcome!\nNote: To end a session press q.\nTo add a new document press a.\n""")
        
        while True:
            data = input("Query: ")
            if data.lower() == 'q':
                print("CONNECTION CLOSED!")
                break
            elif data.lower() == 'a':
                print("Provide the filename...\n")
                server.send(data.encode())
            else:
                server.send(data.encode())
            full_message = ""
            while True:
                chunk = server.recv(2048)
                if not chunk:
                    break
                full_message += chunk.decode()
                if len(chunk) < 2048:
                    break
            print(f"Response: {full_message}\n")
except:
    print("\nCONNECTION CLOSED!")