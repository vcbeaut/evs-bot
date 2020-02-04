# coding:utf-8
 
import select
import socket
import Queue
from time import sleep
import sys
reload(sys)
sys.setdefaultencoding('utf8')  

server = None
# Sockets from which we expect to read
inputs = None
connection = None
client_address = None
readable = None
writable = None
exceptional = None
# Sockets to which we expect to write
# 处理要发送的消息
outputs = []



def ssocket_init():
    # Create a TCP/IP
    global server,inputs
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as msg:
        server = None
        print('create socket failed')
        sys.exit(1)
    inputs = [server]
    server.setblocking(False)

def ssocket_bind_and_listen(IP,PORT,LISTEN_NUM=5):
    # Bind the socket to the port
    server_address = (IP, PORT)
    print ('starting up on %s port %s' % server_address)
    global server
    try:
        server.bind(server_address)
        # Listen for incoming connections
        server.listen(LISTEN_NUM)
    except socket.error as msg:
        server.close()
        server = None
        print('bind and listen socket failed')
        sys.exit(1)

def ssocket_select():
    global readable, writable, exceptional
    print ('waiting for the next event')
    # 开始select 监听, 对input_list 中的服务器端server 进行监听
    # 一旦调用socket的send, recv函数，将会再次调用此模块
    readable, writable, exceptional = select.select(inputs, outputs, inputs)
    #readalbe和server相同

    # # Handle "exceptional conditions"
    # 处理异常的情况
    for s in exceptional:
        print ('exception condition on', s.getpeername())
        # Stop listening for input on the connection
        inputs.remove(s)
        if s in outputs:
            outputs.remove(s)
        s.close()

def ssocket_accept():
    global connection,client_address
    for s in readable:
        if s is server:
            try:
                connection, client_address = s.accept()
                print ('connection from', client_address)
            except socket.error as msg:
                connection = None
                print('accept socket failed')
                sys.exit(1)

    # this is connection not server
    connection.setblocking(0)
    # 将客户端对象也加入到监听的列表中, 当客户端发送消息时 select 将触发
    inputs.append(connection)

def ssocket_read(block=1024):
    global connection,client_address
    # 有老用户发消息, 处理接受
    # 由于客户端连接进来时服务端接收客户端连接请求，将客户端加入到了监听列表中(input_list), 客户端发送消息将触发
    # 所以判断是否是客户端对象触发

    try:
        data = s.recv(block)
    except socket.error as msg:
        print('recv socket exception')
        # sys.exit(1)

    # 客户端未断开
    if data != '':
        # 将需要进行回复操作socket放到output 列表中, 让select监听
        print('recv 1024 data')
        if s not in outputs:
            outputs.append(s)
        return data
    else:
        # 客户端断开了连接, 将客户端的监听从input列表中移除
        # Stop listening for input on the connection
        print('client disconnection')
        if s in outputs:
            outputs.remove(s)
        inputs.remove(s)
        s.close()
        return None

def ssocket_write(data):
    # Handle outputs
    # 如果现在没有客户端请求, 也没有客户端发送消息时, 开始对发送消息列表进行处理, 是否需要发送消息
    try:
        s.send(data)
    except socket.error as msg:
        print('send socket exception')
        # sys.exit(1)




if __name__ == '__main__':
    ssocket_init()
    ssocket_bind_and_listen('0.0.0.0',8010)
    while inputs:
        # Wait for at least one of the sockets to be ready for processing
        ssocket_select()
        for s in readable:
            if s is server:
                ssocket_accept()
            else:
                ret_data = ssocket_read()
                # ssocket_write(b'my send data')
        sleep(1)