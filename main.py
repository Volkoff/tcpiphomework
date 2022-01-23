import configparser
import ipaddress
import socket
import threading
from configparser import ConfigParser

dictionary = {
    "dog" : "pes",
    "cat" : "kocour",
    "parrot" : "papousek",
    "table" : "stul",
    "phone" : "mobil"
}

config = ConfigParser()
config.read('info.conf')
def log(message):
    with open('log.txt','a') as file:
        file.write(message + "\r\n")
        file.close()


def ipranger():
    a = [str(ip) for ip in ipaddress.IPv4Network(f"{config['IPINFO']['ip']}/{config['IPINFO']['mask']}")]
    return a


def translateloc(message, conn):
    try:
        conn.send(f'TRANSLATESUC"{dictionary[message]}"\r\n'.encode('utf-8'))
    except KeyError:
        conn.send('TRANSLATEERR"not in this dictionary"\r\n'.encode("utf-8"))
portsOpen = []
ipport = []


def translateany(conn,message,ip,port):
    if message[1] in dictionary:
        translateloc(message[1],conn)
    else:
        for i in range(len(ipport)):
            t = threading.Thread(target=translaterem, args=(conn, message, ip, port))
            threads.append(t)
            t.start()
            t.join()


iplist = ipranger()
def checkipconnect(portstart,portend,i):
    for port in range(portstart, portend):
        try:
            if i == '192.168.1.110':
                return
            serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            serv.settimeout(3)
            serv.connect((i, port))
            serv.recv(1024)
            serv.send('check'.encode())
            message = serv.recv(1024)
            if message.decode('utf-8') == 'hello':
                log("Hey look! I found it!")
                log(ip + ":" + str(port))
                ipport.append(i + ":" + str(port))
                return
        except Exception as e:
            log(str(e))


def translaterem(conn,message,ip,port):
    try:
        serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serv.connect((ip, port))
        serv.recv(1024)
        serv.send(f'TRANSLATELOC"{message[1]}"'.encode('utf-8'))
        data = serv.recv(1024)
        conn.send(data)
        serv.close()
    except Exception as e:
        log(str(e))



threads = []
def clinet(conn):
    global running
    running = True
    log(f"Connection Established - {address[0]}:{address[1]}")
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
        except Exception as e:
            log(e)
        if message[0] == 'addrem':
            conn.send("working... \r\n".encode('utf-8'))
            for i in ipranger():
                t = threading.Thread(target=checkipconnect, args=(65530, 65536,i))
                threads.append(t)
            for x in threads:
                x.start()
            for x in threads:
                x.join()
            conn.send("SUCCESFUL \r\n".encode('utf-8'))
        elif message[0] == 'check':
            conn.send("hello".encode())
        elif message[0] == "TRANSLATELOC":
            translateloc(message[1],conn)
        elif message[0] == "TRANSLATEREM":
            try:
                for i in range(len(ipport)):
                    ips = ipport[i]
                    ips = ips.split(":")
                    ip = ips[0]
                    port = ips[1]
                    port = int(port)
                    t = threading.Thread(target=translaterem,args=(conn,message,ip,port))
                    threads.append(t)
                    t.start()
                    t.join()

            except Exception as e:
                log(str(e))
        elif message[0] == "TRANSLATEANY":
            for i in range(len(ipport)):
                ips = ipport[i]
                ips = ips.split(":")
                ip = ips[0]
                port = ips[1]
                port = int(port)
                translateany(conn, message, ip, port)
        else:
            conn.send("Wrong".encode('utf-8'))
        log('received from client: %s' % data.decode("utf-8"))




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