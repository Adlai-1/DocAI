import configparser
import socket

config = configparser.ConfigParser()
config.read("config.ini")

host = str(config["AI"]["local"])
port = int(config["AI"]["port"])

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.connect((host, port))

        print(
            """Welcome!\nNote: To end a session press q.\nTo add a new document press a.\n"""
        )

        while True:
            data = input("Input: ")
            if data.lower() == "q":
                print("CONNECTION CLOSED!")
                break

            elif data.lower() == "a":
                file = input("Provide the filename: ")
                if file.endswith(".pdf"):
                    server.send(file.encode())
                    resp = server.recv(1024)
                    print(f"{resp.decode()}\n")
                else:
                    print("Wrong file type provided!")
                continue

            else:
                server.send(data.encode())

            full_message = ""

            while True:
                chunk = server.recv(1024)
                if not chunk:
                    break
                full_message += chunk.decode()
                if len(chunk) < 1024:
                    break
            print(f"Response: {full_message}\n")
except:
    print("\nCONNECTION CLOSED!")
