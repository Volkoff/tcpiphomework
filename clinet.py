import threading
from checkip import Checkip
from commands import Commands


class Clinet:
    welcome_string = "Hey there!!!"
    threads = []
    checkip = Checkip()
    commands = Commands()


    def clinet(self,conn,address):
        global running
        running = True
        self.commands.log(f"Connection Established - {address[0]}:{address[1]}")
        conn.send(self.welcome_string.encode())
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
                self.commands.log(e)
            if message[0] == 'addrem':
                conn.send("working... \r\n".encode('utf-8'))
                for i in self.checkip.ipranger():
                    t = threading.Thread(target=self.checkip.checkipconnect, args=(65530, 65536,i))
                    Commands.threads.append(t)
                for x in self.commands.threads:
                    x.start()
                for x in self.commands.threads:
                    x.join()
                conn.send("SUCCESFUL \r\n".encode('utf-8'))
            elif message[0] == 'check':
                conn.send("hello".encode())
            elif message[0] == "TRANSLATELOC":
                Commands.translateloc(message[1],conn)
            elif message[0] == "TRANSLATEREM":
                try:
                    for i in range(len(Checkip.ipport)):
                        ips = self.checkip.ipport[i]
                        ips = ips.split(":")
                        ip = ips[0]
                        port = ips[1]
                        port = int(port)
                        t = threading.Thread(target=self.commands.translaterem,args=(conn,message,ip,port))
                        self.commands.threads.append(t)
                        t.start()
                        t.join()

                except Exception as e:
                    self.commands.log(str(e))
            elif message[0] == "TRANSLATEANY":
                for i in range(len(self.checkip.ipport)):
                    ips = self.checkip.ipport[i]
                    ips = ips.split(":")
                    ip = ips[0]
                    port = ips[1]
                    port = int(port)
                    self.commands.translateany(conn, message, ip, port)
            else:
                conn.send("Wrong".encode('utf-8'))
            self.commands.log('received from client: ' + data.decode("utf-8"))
