# -*- coding: utf-8 -*-
# create time    : 2021-01-06 15:52
# author  : CY
# file    : voice_client.py
# modify time:
import os
import socket
import sys
import threading
import time

import pyaudio
from PyQt6 import QtWidgets
from pydub import AudioSegment
from pydub.playback import play

from UI import Ui_MainWindow, UI_LoginWindow

from tkinter import messagebox as msgbox


class Client:
    def __init__(self, target_ip='26.214.15.89', target_port=11451):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ts = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.target_ip = target_ip
        self.target_port = int(target_port)
        print(self.target_ip, self.target_port)
        while 1:
            try:
                self.s.connect((self.target_ip, self.target_port))

                self.ts.connect((self.target_ip, self.target_port + 1))

                break
            except Exception as e:
                print(e)
                print("Couldn't connect to server")
                msgbox.showerror("Error", "Couldn't connect to server")
                sys.exit("Couldn't connect to server")

        chunk_size = 512  # 512
        audio_format = pyaudio.paInt16
        channels = 1
        rate = 40000

        self.p = pyaudio.PyAudio()
        self.playing_stream = self.p.open(format=audio_format, channels=channels, rate=rate, output=True,
                                          frames_per_buffer=chunk_size)
        self.recording_stream = self.p.open(format=audio_format, channels=channels, rate=rate, input=True,
                                            frames_per_buffer=chunk_size)

        print("Connected to Server")

        # start threads
        receive_thread = threading.Thread(target=self.receive_server_data)
        receive_thread.daemon = True
        receive_thread.start()
        send_thread = threading.Thread(target=self.send_data_to_server)
        send_thread.daemon = True
        send_thread.start()
        ping_thread = threading.Thread(target=self.ping)
        ping_thread.daemon = True
        ping_thread.start()

    def receive_server_data(self):
        rate = 20000
        while True:
            try:
                data = self.s.recv(512)
                if ui.check2_state() and len(data) > 20:
                    self.playing_stream.write(data)

            except Exception as e:
                if "WinError 10054" in str(e):
                    sys.exit(str(e))
                else:
                    print(e)
                pass

    def send_data_to_server(self):
        while True:
            try:
                data = self.recording_stream.read(512)
                if ui.check1_state():
                    self.s.sendall(data)
            except:
                pass

    def ping(self):
        global ui
        while True:
            try:
                data = self.ts.recv(1024).decode('utf-8')
                #
                #if data == "exit":
                #    msgbox.showinfo("Exit", "Server shutting down")
                #    sys.exit(0)
                ui.change_text(int(data) - int(round(time.time() * 1000)))
            except:
                ui.change_text("连接ping服务器失败")


if __name__ == '__main__':
    lwin = UI_LoginWindow()
    ip, port = lwin.__str__()
    global ui
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow(MainWindow)
    MainWindow.show()
    client = Client(ip, port)
    sys.exit(app.exec())
