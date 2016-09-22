'''
Created on 10 Eyl 2016

@author: erkan
'''

import socket
import threading
from multiprocessing import Queue, Process
import time
import serial
import logging
import datetime
from _collections import defaultdict


class message(object):
#     self.time
#     self.messageNo
#     self.body
    mes_index = {}
    def __init__(self,data = None, messageNo = None, messageBody = None):
        if data is not None:            
            if data[0] == '<':
                data.lstrip('<')
                data.rstrip('>')
                data = data.split("|")
                dt = datetime.datetime.now()
                self.time = dt.microsecond
                self.messageNo = data[0]
                self.body = data[1]
                #message.mes_list

            else:
                raise ValueError('bad data')
        
        else:
            self.messageNo = messageNo
            self.messageBody = messageBody
            dt = datetime.datetime.now()
            self.time = dt.microsecond
            
        #message.mes_index[self.messageNo] = self
    
#     @classmethod    
#     def find(cls, no):
#         return message.mes_index[no]
        
        

class tester(object):
    '''
    classdocs
    '''
    

    def __init__(self):
        '''
        Constructor
        '''
        print("create test connection")
        
        #logger = logging()
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.data = "1234567890"
        #To Test server application
        #self.sock.connect(('localhost',4444))
        self.sock.connect(('127.0.0.1',4444))
        
        
        self.socketReceiveQueue = Queue(1024)
        self.socketSendQueue = Queue(1024)
        self.serialReceiveQueue = Queue(1024)
        self.serialSendQueue = Queue(1024)
        #self.data = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin at nibh sem. Vivamus aliquam turpis dolor, in elementum libero vulputate vel. Suspendisse id eros in massa ultrices scelerisque. Maecenas eu eros eget odio elementum dictum eu vitae eros. Nullam suscipit cursus nibh, vel congue massa mattis eget. Suspendisse hendrerit ac mi id cursus. Aliquam porta efficitur enim quis bibendum. Fusce ut placerat lacus, eu tincidunt ipsum. Maecenas et viverra mauris. Vivamus sit amet posuere odio. Fusce rhoncus diam at accumsan luctus. Donec ac suscipit sapien. Duis ullamcorper eget sem a ultricies. In vitae congue sem. Phasellus viverra sollicitudin orci, non malesuada odio rutrum vel. Vivamus quis pretium est, at bibendum arcu. Praesent lobortis odio elit, rhoncus bibendum tellus finibus id. Sed quis justo hendrerit, pharetra mauris et, tincidunt quam. Quisque laoreet, sem non luctus interdum, mi neque finibus odio, ac vulputate augue sapien vitae ipsum. Sed a semper arcu. In est lacus, laoreet sed quam eu, pharetra placerat neque. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Aliquam ante arcu, pellentesque in ultrices ac, euismod non eros. Cras sem risus, dignissim eget sollicitudin eu, vehicula eget eros. Sed vestibulum varius consectetur. Duis sed tellus vel magna pretium auctor nec at urna. Etiam blandit arcu at magna dictum tincidunt. Mauris gravida convallis justo. Donec non justo ullamcorper, scelerisque enim quis, consectetur tortor. Sed iaculis vel lacus vitae feugiat. Donec vulputate ex massa, id laoreet mi rhoncus non. Maecenas vitae vehicula sapien. Fusce interdum molestie ante, in laoreet velit accumsan a. Ut sodales tempus mauris vitae interdum. Nulla ullamcorper dolor risus, vitae molestie lectus placerat non. Fusce luctus gravida leo a dignissim. Aliquam convallis sem et ultricies consectetur. Praesent blandit, odio at vulputate feugiat, elit lacus consequat nisi, a sodales ligula orci porta ipsum. Quisque in diam nibh. Praesent ut dapibus felis. Duis eu quam et diam pulvinar gravida in at felis. Cras odio orci, luctus ac ipsum id, ultrices maximus ex. Nulla faucibus cursus orci, vitae maximus justo. Vivamus quis mauris ut diam pretium venenatis. Donec quis elit consectetur, finibus nisl at, rutrum leo. "
        #init serial interface
        self.com = serial.Serial()
#         self.socketSendList = []
#         self.serialSendList = []
#         self.socketReceiveList = []
#         self.serialReceiveList = []
        self.socketSendList = {}
        self.serialSendList = {}
        self.socketReceiveList = {}
        self.serialReceiveList = {}
        try:
            self.com = serial.Serial()
            self.com.baudrate = 115200
            self.com.port = "com17"
            self.com.rts = False
            self.com.parity = serial.PARITY_NONE
            self.com.stopbits = serial.STOPBITS_ONE
            self.com.bytesize = 8
            self.com.open()
        except Exception as msg:
            print("HATA: " + str(msg))
            
        if self.com.isOpen():
            print("serial port opened")
        
        t2 = threading.Thread(target=self.testSocketRecieveThread)
        t2.start()
        
        t1 = threading.Thread(target=self.testSerialSendThread)
        t1.start()
#         t3 = threading.Thread(target=self.testSocketSendThread)
#         t3.start()

        
    
    def connect(self, address, portNo):
        self.sock.connect((address, portNo))
        
    
    def startTest(self):
        t1 = threading.Thread(target=self.testSocketSendThread)
        t1.start()
        t3 = threading.Thread(target=self.testHandlerThread)
        t3.start()

    def testSocketRecieveThread(self):
        print("receive thread started")
        while True:
            received = self.sock.recv(1024)
            receivedSTR = received.decode("UTF-8")
    #         if receivedSTR[0] == '<':
    #             receivedSTR.lstrip('<')
    #             receivedSTR.rstrip('>')
    #             receivedSTR = receivedSTR.split("|")
            print(receivedSTR)
            #self.socketReceiveQueue.put(receivedSTR)
    #         try:
    #             
    #             receivedMes = message(receivedSTR)
    #             self.socketReceiveList[receivedMes.messageNo] = receivedMes
    #             #self.socketReceiveList.append(receivedMes)
    #             print(receivedSTR[0])
    #         except:
    #             print('BAd Data')
    
    def testSocketSendThread(self):
        print("send thread starting...\n")
        messageNo = 0
        while True:
            sent = self.sock.send(bytes("<" + str(messageNo) +"|" + self.data + ">"))
            if sent > 0:
                #self.socketSendQueue.put(messageNo)
                mes = message(messageNo=messageNo,messageBody=self.data)
                self.socketSendList[mes.messageNo] = mes
                messageNo = messageNo + 1
                time.sleep(1)
    
    def testSerialSendThread(self):
        print("serial Send task")
        messageNo = 0
        while True:
            print("send data")
            dataToSend = bytes("<" + str(messageNo) +"|" + self.data + ">\r\n")
            self.com.write(dataToSend)
            messageNo = messageNo + 1
            time.sleep(2)
            
            
    def serialReceive(self):
        pass
    
    def testHandlerThread(self):
        
        while True: 
#             if not self.socketSendQueue.empty():
#                 item = self.socketSendQueue.get()
#                 print("item: " + str(item) + " has sent")
#                 self.socketSendList.Append(item)
                
            if not self.serialSendQueue.empty():
                item = self.serialSendQueue.get()
                self.serialSendList.Append(item)
                
            if not self.socketReceiveQueue.empty():
                pass

                    
            if not self.serialReceiveQueue.empty():
                receivedSTR = self.socketReceiveQueue.get()
                receivedMes = message(data=receivedSTR) 
                try:
                    if self.socketSendList[receivedMes.messageNo] == self.data:
                        print(receivedMes.messageNo + " received successfully")
                    else:
                        #log it!
                        print("something wrong")
                except:
                    print("bad data has arrived")
                    #log it!
               
                #items.append(item)
            
            
#             if not self.socketReceiveQueue.empty():
#                 item = self.socketReceiveQueue.get()
#                 if item[1] != self.data:
#                     print("error at transmit")
#                 else:and print("transmit ok")
                
            pass
        
    def openComport(self):
        pass