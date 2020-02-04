from websocket_server import WebsocketServer
from threading import Thread
import p_call_c
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

def web_show(str,flag):
    print("py:"+str)
    print("flag:"+flag)
    if flag == "ING":
        server.send_message_to_all("ING")
    elif flag == "ED":
        server.send_message_to_all("ED")
    server.send_message_to_all(str)

if __name__ == '__main__':
    thread_websocket = Thread(target=start_websocket)
    thread_websocket.start()
    
    