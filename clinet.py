import threading
from checkip import Checkip
from commands import Commands


class Clinet:
    welcome_string = "Hey there!!!"
    threads = []

    def log(message):
        with open('log.txt','a') as file:
            file.write(message + "\r\n")
            file.close()

    def clinet(self,conn,address):
        global running
        running = True
        Commands.log(f"Connection Established - {address[0]}:{address[1]}")
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
                Commands.log(e)
            if message[0] == 'addrem':
                conn.send("working... \r\n".encode('utf-8'))
                for i in Checkip.ipranger():
                    t = threading.Thread(target=Commands.Checkipconnect, args=(65530, 65536,i))
                    Commands.threads.append(t)
                for x in Commands.threads:
                    x.start()
                for x in Commands.threads:
                    x.join()
                conn.send("SUCCESFUL \r\n".encode('utf-8'))
            elif message[0] == 'check':
                conn.send("hello".encode())
            elif message[0] == "TRANSLATELOC":
                Commands.translateloc(message[1],conn)
            elif message[0] == "TRANSLATEREM":
                try:
                    for i in range(len(Checkip.ipport)):
                        ips = Checkip.ipport[i]
                        ips = ips.split(":")
                        ip = ips[0]
                        port = ips[1]
                        port = int(port)
                        t = threading.Thread(target=Commands.translaterem,args=(conn,message,ip,port))
                        Commands.threads.append(t)
                        t.start()
                        t.join()

                except Exception as e:
                    Commands.log(str(e))
            elif message[0] == "TRANSLATEANY":
                for i in range(len(Checkip.ipport)):
                    ips = Checkip.ipport[i]
                    ips = ips.split(":")
                    ip = ips[0]
                    port = ips[1]
                    port = int(port)
                    Commands.translateany(conn, message, ip, port)
            else:
                conn.send("Wrong".encode('utf-8'))
            Commands.log('received from client: %s' % data.decode("utf-8"))
