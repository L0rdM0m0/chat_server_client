#!/usr/bin/env python3

import socket
import sys
import subprocess
from threading import Thread

def client_connect():
    try:
        soc.connect((host, port))
    except:
        print("Unable to connect")
        sys.exit()

    print ('Client 2.0\n')
    print ('Welcome to the chat room')
    print ("Enter 'quit' to exit\n")
    message = ('')
    try:
        Thread(target=read_thread).start()
    except:
        print ('Unable to create thread')

    name = input(str('Enter your name : '))
    con_msg = name + ' has joined the chat room'
    soc.sendall(bytes(con_msg, 'utf-8'))

    while message.upper() != 'QUIT':
    	while message == "":
    		message = input(str('[Me] '))
    	soc.sendall(bytes(message, 'utf-8'))
    	message = input(str('[Me] '))



    soc.sendall(bytes(message, 'utf-8'))
    soc.close()

def read_thread(max_buffer_size = 1024):

    while True:
        server_input = soc.recv(max_buffer_size)
        server_mes = str(server_input.decode('utf-8'))
        print (server_mes)
        print ('[Me] ', end = '', flush=True )

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "127.0.0.1"
port = 65432
subprocess.call('clear', shell=True)
client_connect()
