import socket
import threading
import time

tLock = threading.Lock()
shutdown = False
host = '127.0.0.1'
port = 0

server = ('127.0.0.1',5000)

def receving(name, sock):
    while not shutdown:
        try:
            tLock.acquire()
            while True:
                data, addr = sock.recvfrom(1024)
                print str(data)
        except:
            pass
        finally:
            tLock.release()

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))
s.setblocking(0)

rT = threading.Thread(target=receving, args=("RecvThread",s))
rT.start()

username = raw_input("Username: ")
message = raw_input(username + "-> ")
while message != 'q':
    if message != '':
        s.sendto(username + ": " + message, server)
    tLock.acquire()
    message = raw_input(username + "-> ")
    tLock.release()
    time.sleep(0.2)

shudown = True
rT.join()
s.close()