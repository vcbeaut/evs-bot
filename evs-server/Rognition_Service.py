import socket

import ctypes
from ctypes import *
import signal
from websocket_server import WebsocketServer
from threading import Thread

dllObj = ctypes.cdll.LoadLibrary('samples.dll')
sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_server.bind(("0.0.0.0",8010))
sock_server.listen(5)

def new_client(client, server):
	print("New client connected and was given id %d" % client['id'])
	server.send_message_to_all("hello,snowboy!")

# Called for every client disconnecting
def client_left(client, server):
	print("Client(%d) disconnected" % client['id'])

def start_websocket():
    PORT=8020
    global server
    server = WebsocketServer(PORT)
    print('listenin websoket port:8020')
    server.set_fn_new_client(new_client)
    server.set_fn_client_left(client_left)
    server.run_forever()


def Translation_Recognition():
    while True:
        print('listening socket port:8010')
        conn,address = sock_server.accept()
        print('connect_success')
        
        dllObj.Translation_Open()
        wf = open('recv.wav','wb')
        print('traslating')
        while True:
            try:
                data = conn.recv(1024)
            except socket.error:
                pass

            if not data:
                break
            # print('recv 1024')
            dllObj.Translation_Write(data,len(data))
            wf.write(data)
        print('recv finished')
        wf.close()
        conn.close()
        dllObj.Translation_Close()
        # libHandle = dllObj._handle
        # del dllObj
        # ctypes.windll.kernel32.FreeLibrary(libHandle)

def Speech_Recognition():
    while True:
        print('connect_wait,listening 8010')
        conn,address = sock_server.accept()
        print('connect_success')
        
        dllObj.Speech_Open()
        wf = open('recv.wav','wb')
        print('speeching')
        while True:
            try:
                data = conn.recv(1024)
            except socket.error:
                pass
            except KeyboardInterrupt:
                exit()
            if not data:
                break
            # print('recv 1024')
            dllObj.Speech_Write(data,len(data))
            wf.write(data)
        print('recv finished')
        wf.close()
        conn.close()
        dllObj.Speech_Close()

def Rog_Speech(str,flag):
    print("py:"+str)
    print("flag:"+flag)
    if flag == "ING":
        server.send_message_to_all("ING")
    elif flag == "ED":
        server.send_message_to_all("ED")

    server.send_message_to_all(str)

functype = ctypes.CFUNCTYPE(None,ctypes.c_char_p,ctypes.c_char_p)
dllcallback = functype(Rog_Speech)
dllObj.set_call(dllcallback)

if __name__ == '__main__':
    thread_websocket = Thread(target=start_websocket)
    thread_websocket.start()
    Speech_Recognition()
    #Translation_Recognition()