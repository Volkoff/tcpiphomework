import socket
import threading

dictionary = {
    "dog" : "pes",
    "cat" : "kocour",
    "parrot" : "papousek",
    "table" : "stul",
    "phone" : "mobil"
}

portsOpen = []
def clinet(conn):
    global running
    running = True
    print(f"Connection Established - {address[0]}:{address[1]}")
    conn.send(welcome_string.encode())
    while running:
        data = conn.recv(1024)
        if not data or data.decode('utf-8').lower() == 'end':
            break
        str = data.decode('utf-8')
        str = str.split('"')
        if str[0] == "TRANSLATELOC":
            try:
                conn.send(dictionary[str[1]].encode('utf-8'))
            except KeyError:
                conn.send('TRANSLATEERR"not in this dictionary"'.encode("utf-8"))
        if str[0] == "TRANSLATEREM":
            try:
                for i in range(256):
                    ip = "127.0.0.%d" % i
                    for port in range(65530, 65536):
                        try:
                            print(ip)
                            print(port)
                            serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            serv.connect((ip, port))
                            serv.recv(1024)
                            serv.send('test'.encode('utf-8'))
                            serv.recv(1024)
                            portsOpen.append(port)
                        except Exception as e:
                            print(e)
                serv.connect((ip,portsOpen[0]))
                serv.recv(1024)
                serv.send(f'TRANSLATELOC"{str[1]}"'.encode('utf-8'))
                data = serv.recv(1024)
                conn.send(data)
                print(portsOpen)
            except:
                print("OOF")
        else:
            conn.send("Wrong".encode('utf-8'))
        print('received from client: %s' % data.decode("utf-8"))



welcome_string = "Hey there!!!"
ip = '127.0.0.1'
port = 65532
HEADER_LENGTH = 1024
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((ip, port))
server.listen(5)
while True:
    conn, address = server.accept()
    print("connecdtedd")
    t1 = threading.Thread(target=clinet, args = (conn,))
    t1.start()