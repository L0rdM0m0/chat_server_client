#!/usr/bin/env python3

import socket
import sys
import traceback
import subprocess
from threading import Thread

def server():
    host = "127.0.0.1"
    port = 65432
    subprocess.call('clear', shell=True)
    print ('Server 2.0\n')

    try:
        print ('Welcome to the chat server')
        print ('Initialising....\n')
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        soc.bind((host,port))
    except:
        print ('Unable to bind to ' + host + " " + str(port))
        sys.exit()

    soc.listen(3)       
    print('Server is listening on port ' + str(port) +'\n')

    while True:
        conn, addr = soc.accept()
        connected_clients.append(conn)
        print ('Server connected to client ' + str(addr[0]) + " " + str(addr[1]))
        client_message = ('Client connected from : ' + str(addr[0]) + " " + str(addr[1]))

        try:
            Thread(target=client_thread, args=(conn, addr)).start()
        except:
            print('Unable to create a thread')
            traceback.print_exc()

    soc.close()


def client_thread(connection, addr, max_buffer_size = 1024):
    client_input = connection.recv(max_buffer_size)
    client_input = '[SERVER] ' + str(client_input.decode('utf-8'))
    client_wordlist = client_input.split()
    client_name = client_wordlist[1]
    print (client_input + " " + str(addr[0]) + " " + str(addr[1]))
    broadcast_message(client_input,connection)

    while True:
        client_input = connection.recv(max_buffer_size)
        all_message = '[' + client_name + ']' + " " + str(client_input.decode('utf-8'))

        if all_message.split(" ")[-1].upper() == 'QUIT':
            close_mess = '[SERVER] ' + client_name + ' left the chat room'
            print (close_mess)
            broadcast_message(close_mess,connection)
            connected_clients.remove(connection)
            break

        print (all_message)
        broadcast_message(all_message,connection)

def broadcast_message(message,conn):
    for x in range(0,len(connected_clients)):
        if conn != connected_clients[x]:
            connected_clients[x].sendall(bytes(message, 'utf-8'))
        

try:
    connected_clients = []
    server()
except KeyboardInterrupt:
    print ('Interrupted, closing the socket and quitting')
    sys.exit(0)
