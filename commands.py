import threading
from socket import socket


class Commands:
    def log(message):
        with open('log.txt', 'a') as file:
            file.write(message + "\r\n")
            file.close()

    dictionary = {
        "dog" : "pes",
        "cat" : "kocour",
        "parrot" : "papousek",
        "table" : "stul",
        "phone" : "mobil"
    }

    def translateloc(self,message, conn):
        try:
            conn.send(f'TRANSLATESUC"{self.dictionary[message]}"\r\n'.encode('utf-8'))
        except KeyError:
            conn.send('TRANSLATEERR"not in this dictionary"\r\n'.encode("utf-8"))

    ipport = []

    threads = []
    def translateany(self,conn,message,ip,port):
        if message[1] in self.dictionary:
            self.translateloc(message[1],conn)
        else:
            for i in range(len(self.ipport)):
                t = threading.Thread(target=self.translaterem, args=(conn, message, ip, port))
                self.threads.append(t)
                t.start()
                t.join()




    def translaterem(self,conn,message,ip,port):
        try:
            serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            serv.connect((ip, port))
            serv.recv(1024)
            serv.send(f'TRANSLATELOC"{message[1]}"'.encode('utf-8'))
            data = serv.recv(1024)
            conn.send(data)
            serv.close()
        except Exception as e:
            self.log(str(e))
