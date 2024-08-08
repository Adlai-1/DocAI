import socket
import os, sys
import configparser
sys.path.append(os.path.abspath(os.path.dirname("rag_model")))
from rag_model.model import call_rag

config = configparser.ConfigParser()
config.read("config.ini")

host = str(config['AI']['local'])
port = int(config['AI']['port'])

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind((host, port)) 
    print("Server up and running!")
    chats = []
    server.listen() 
    conn, addr = server.accept()
    print(f"Connection established with {addr}") 
    
    while True:
        data = conn.recv(2048)
        if not data: break
        if data.decode() == 'a':
            conn.send("Provide a filename: ")
        else:
            try:
                resp = call_rag(data.decode(), chats)
                for i in range(0, len(resp), 2048):
                    conn.send(resp[i:i + 2048].encode())
            except:
                conn.send("Unable to generate a response. Try again later!")