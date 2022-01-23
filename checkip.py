import ipaddress
from configparser import ConfigParser
from socket import socket
from commands import Commands


class Checkip:
    def log(message):
        with open('log.txt','a') as file:
            file.write(message + "\r\n")
            file.close()


    config = ConfigParser()
    config.read('info.conf')


    a = [str(ip) for ip in ipaddress.IPv4Network(f"{config['IPINFO']['ip']}/{config['IPINFO']['mask']}")]


    ipport = []
    iplist = a
    def checkipconnect(self,portstart,portend,i):
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
                    Commands.log("Hey look! I found it!")
                    Commands.log(i + ":" + str(port))
                    self.ipport.append(i + ":" + str(port))
                    return
            except Exception as e:
                Commands.log(str(e))
