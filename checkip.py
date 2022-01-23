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

    def ipranger(self):
        a = [str(ip) for ip in ipaddress.IPv4Network(f"{self.config['IPINFO']['ip']}/{self.config['IPINFO']['mask']}")]
        return  a
    commands = Commands()
    ipport = []
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
                    self.commands.log("Hey look! I found it!")
                    self.commands.log(i + ":" + str(port))
                    self.ipport.append(i + ":" + str(port))
                    return
            except Exception as e:
                self.commands.log(str(e))
