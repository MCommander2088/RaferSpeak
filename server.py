# -*- coding: utf-8 -*-
# create time    : 2020-12-30 15:37
# author  : CY
# file    : voice_server.py
# modify time:
import socket
import threading
import time


class Server:
    def __init__(self):
        self.ip = socket.gethostbyname(socket.gethostname())
        while True:
            try:
                self.port = 11451
                self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.s.bind((self.ip, self.port))
                break
            except:
                print("Couldn't bind to that port")

        self.connections = []
        self.accept_connections()

    def accept_connections(self):
        self.s.listen()

        print('Running on IP: ' + self.ip)
        print('Running on port: ' + str(self.port))

        while True:
            c, addr = self.s.accept()

            self.connections.append(c)

            threading.Thread(target=self.handle_client, args=(c, addr,)).start()

    def broadcast(self, sock, data):
        for client in self.connections:
            if client != self.s and client != sock:
                try:
                    client.send(data)
                    #client.send(str(int(round(time.time() * 1000))).encode('utf-8'))
                except:
                    pass

    def handle_client(self, c, addr):
        while 1:
            try:
                data = c.recv(512)
                self.broadcast(c, data)

            except socket.error:
                c.close()

if __name__ == '__main__':
    server = Server()