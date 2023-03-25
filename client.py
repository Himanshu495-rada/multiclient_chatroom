import curses
from curses import wrapper
import time
import socket
import threading
from msvcrt import kbhit, getwch as _getch

status = True

def receive(stdscr, s):
    i = 1
    global status
    while status:
        data = s.recv(1024)
        stdscr.addstr(i, 0, data.decode("utf-8"))

        #move cursor to 0,0
        stdscr.move(0,3)
        stdscr.refresh()
        i += 1
        time.sleep(1)

def main(stdscr):
    stdscr.clear()
    curses.echo()

    stdscr.addstr(0,0, "Enter your name: ")
    name = stdscr.getstr(0, 17, 100)

    stdscr.addstr(2, 0, "Enter host IP: ")
    host = stdscr.getstr(2, 15, 100)
    host = host.decode("utf-8")

    stdscr.addstr(4, 0, "Enter Port: ")
    port = stdscr.getstr(4, 12, 100)
    port = int(port.decode("utf-8"))

    stdscr.addstr(6, 0, "Connecting to " + host + "on port " + str(port) + "........")

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    threading.Thread(target=receive, args=(stdscr, s), daemon=True).start()

    stdscr.clear()
    global status
    while True:
        stdscr.addstr(0, 0, "=> ")
        stdscr.clrtoeol() # clear to end of the line

        data = stdscr.getstr(0, 3, 100)
        if data == b":q": 
            status = False
            break
        else:
            data = name + b": " + data
            s.sendall(data)
            stdscr.refresh()
    stdscr.refresh()

if __name__ == '__main__':
    wrapper(main)
    