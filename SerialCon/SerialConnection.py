'''
Created on 26 Oca 2016

@author: erkan
'''
import serial
import serial.tools.list_ports
import socket, pickle
#import thread
import threading
import time
import test_connection




def listen():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((socket.gethostname()), 4445)
    


def connect_task():
    print("start connetion task")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('192.168.1.107',4444))
    #sock.connect(('192.168.1.107',4444))
    data = "patates"
    while True:
        print("send data: " + data)
        sent = sock.send(bytes("patates",'UTF-8'))
        print("sent: " + str(sent))
        #print ("res: ", sock.recv(1024))
        time.sleep(1)


def serialTask(com):
    print("serial task started")
    while True:
        recCount = com.inWaiting()
        if recCount > 0:
            #print(com.inWaiting())
            received = com.read(recCount)
            print(received.decode("UTF-8"))

ports = list(serial.tools.list_ports.comports())
for p in ports:
    print(p)

print("----------------------------------------------------")

# com = serial.Serial()
# 
# com.baudrate = 115200
# com.port = "com17"
# 
# 
# print("erkan")
# 
# try:
#     com.rts = False
#     com.parity = serial.PARITY_NONE
#     com.stopbits = serial.STOPBITS_ONE
#     com.bytesize = 8
#     com.open()
# except Exception as msg:
#     print("HATA: " + str(msg))
#     
# if com.isOpen():
#     print("opened")
# else:
#     print("port couldnT open")
#     
# # sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# # sock.connect(('localhost',4444))
# # time.sleep(2)
# # sock.close()
# #_thread.start_new_thread(connect_task)
# 
# # t = threading.Thread(target=connect_task)   
# # t.start()
# 
# print("start test\n")
# 
# 
# com.write("deneme\n")
# 
# t1 = threading.Thread(target=serialTask, args = (com,))
# t1.start()
test = test_connection.tester()
#com.close()

# test = test_connection.tester()
# test.connect("localhost", 4444)
# test.startTest()


        
    