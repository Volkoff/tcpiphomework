import ipaddress
from configparser import ConfigParser
from socket import socket

def log(message):
    with open('log.txt','a') as file:
        file.write(message + "\r\n")
        file.close()


config = ConfigParser()
config.read('info.conf')


def ipranger():
    a = [str(ip) for ip in ipaddress.IPv4Network(f"{config['IPINFO']['ip']}/{config['IPINFO']['mask']}")]
    return a

ipport = []
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
                log(i + ":" + str(port))
                ipport.append(i + ":" + str(port))
                return
        except Exception as e:
            log(str(e))
