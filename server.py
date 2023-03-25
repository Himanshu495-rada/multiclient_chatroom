import socket
import threading
from msvcrt import kbhit, getwch as _getch

host = "localhost"
port = 8001
ESC = '\x1b'
status = True

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((host, port))
s.listen(5)

clients = []

def serve(client, status):
    while status:
        try:
            data = client.recv(1024)
            for c in clients:
                if c.fileno() == -1:
                    clients.remove(c)
                    print(c.getpeername()[0], "disconnected 😒")
                    continue
                print("Sending data to ", c.getpeername()[0])
                c.sendall(data)
        except ConnectionResetError:
            clients.remove(client)
            print(client.getpeername()[0], "disconnected")
            break

def accept(stat):
    try:
        while True:
            client, address = s.accept()
            clients.append(client)
            print("Connected to: ", address)

            threading.Thread(target=serve, args=(client, stat), daemon=True).start()
    except:
        print("Listening stopped")

if __name__ == '__main__':
    print("Server started on port: ", port)
    threading.Thread(target=accept, args=(status,)).start()

    while True:
        if kbhit() or _getch() == ESC:
            status = False
            s.close()
            print("Server stopped")
            break
    