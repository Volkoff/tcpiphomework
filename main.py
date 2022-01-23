import socket
import threading
from clinet import Clinet
ip = '192.168.1.110'
port = 65532
HEADER_LENGTH = 1024
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((ip, port))
server.listen(5)
while True:
    conn, address = server.accept()
    print("connecdtedd")
    t1 = threading.Thread(target=Clinet, args = (conn,address))
    t1.start()