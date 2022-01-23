import socket
import threading

dictionary = {
    "dog" : "pes",
    "cat" : "kocour",
    "parrot" : "papousek",
    "table" : "stul",
    "phone" : "mobil"
}


def translateloc(message, conn):
    try:
        conn.send(f'TRANSLATESUC"{dictionary[message]}"\r\n'.encode('utf-8'))
    except KeyError:
        conn.send('TRANSLATEERR"not in this dictionary"\r\n'.encode("utf-8"))
portsOpen = []
ipport = []
def checkipconnect():
    #for i in range(256):
        ip = "192.168.1.107"
        print(ip)
        for port in range(65531, 65533):
            print(port)
            try:
                serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                serv.connect((ip, port))
                serv.settimeout(0.01)
                serv.recv(1024)
                serv.send('check'.encode())
                message = serv.recv(1024)
                print(type(message))
                if message.decode('utf-8') == 'hello':
                    print("hey")
                    ipport.append(ip + ":" + port)
                print(ipport)
            except Exception as e:
                print(e)


# def translaterem(conn):
#     try:
#         checkipconnect()
#         serv.connect((ip, portsOpen[0]))
#         serv.recv(1024)
#         serv.send(f'TRANSLATELOC"{message[1]}"'.encode('utf-8'))
#         data = serv.recv(1024)
#         conn.send(data)
#         print(portsOpen)
#     except Exception as e:
#         print(e)


def clinet(conn):
    global running
    running = True
    print(f"Connection Established - {address[0]}:{address[1]}")
    conn.send(welcome_string.encode())
    while running:
        data = conn.recv(1024)
        if not data or data.decode('utf-8').lower() == 'end':
            break

        if data.decode('utf-8') == "\r\n" or data.decode('utf-8') == "\n":
            data = conn.recv(1024)
        try:
            message = data.decode('utf-8')
            message = str(message)
            message = message.split('"')
            print(message[0])
        except Exception as e:
            print(e)

        if message[0] == 'check':
            conn.send("hello".encode())
        if message[0] == "TRANSLATELOC":
            translateloc(message[1],conn)
        elif message[0] == "TRANSLATEREM":
            checkipconnect()
            print(message[1])
        else:
            conn.send("Wrong".encode('utf-8'))
        print('received from client: %s' % data.decode("utf-8"))



welcome_string = "Hey there!!!"
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
    t1 = threading.Thread(target=clinet, args = (conn,))
    t1.start()