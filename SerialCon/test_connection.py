'''
Created on 10 Eyl 2016

@author: erkan
'''

import socket
import threading
from multiprocessing import Queue
import time
import serial.tools.list_ports
import logging
import traceback


class message(object):
#     self.time
#     self.messageNo
#     self.body
    mes_index = {}
    def __init__(self,data = None, messageNo = None, messageBody = None):
        if data is not None:            
            if data[0] == '<':
                data = data.lstrip('<')
                data = data.rstrip()
                data = data.strip(' \t\n\r')
                data = data.rstrip('>')
#                 print("stripped: "+data)
                data = data.split("|")
                self.time = int(time.time() * 1000)
                self.messageNo = int(data[0])
                self.body = data[1]
                #message.mes_list

            else:
                raise ValueError('bad data')
        
        else:
            self.messageNo = messageNo
            self.messageBody = messageBody
            self.time = int(time.time() * 1000)
            
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
        IP_ADDRESS = '192.168.1.113'
        COM_PORT = "/dev/ttyUSB0"
        
        #logger = logging()
        logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', datefmt='%d.%m.%Y %H:%M:%S ', filename='s2e.log',level=logging.DEBUG)
        
       
        #self.data = "123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890"
        self.data = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin at nibh sem. Vivamus aliquam turpis dolor, in elementum libero vulputate vel. Suspendisse id eros in massa ultrices scelerisque. Maecenas eu eros eget odio elementum dictum eu vitae eros. Nullam suscipit cursus nibh, vel congue massa mattis eget. Suspendisse hendrerit ac mi id cursus. Aliquam porta efficitur enim quis bibendum. Fusce ut placerat lacus, eu tincidunt ipsum. Maecenas et viverra mauris. Vivamus sit amet posuere odio. Fusce rhoncus diam at accumsan luctus. Donec ac suscipit sapien. Duis ullamcorper eget sem a ultricies. In vitae congue sem. Phasellus viverra sollicitudin orci, non malesuada odio rutrum vel. Vivamus quis pretium est, at bibendum arcu. Praesent lobortis odio elit, rhoncus bibendum tellus finibus id. Sed quis justo hendrerit, pharetra mauris et, tincidunt quam. Quisque laoreet, sem non luctus interdum, mi neque finibus odio, ac vulputate augue sapien vitae ipsum. Sed a semper arcu. In est lacus, laoreet sed quam eu, pharetra placerat neque. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Aliquam ante arcu, pellentesque in ultrices ac, euismod non eros. Cras sem risus, dignissim eget sollicitudin eu, vehicula eget eros. Sed vestibulum varius consectetur. Duis sed tellus vel magna pretium auctor nec at urna. Etiam blandit arcu at magna dictum tincidunt. Mauris gravida convallis justo. Donec non justo ullamcorper, scelerisque enim quis, consectetur tortor. Sed iaculis vel lacus vitae feugiat. Donec vulputate ex massa, id laoreet mi rhoncus non. Maecenas vitae vehicula sapien. Fusce interdum molestie ante, in laoreet velit accumsan a. Ut sodales tempus mauris vitae interdum. Nulla ullamcorper dolor risus, vitae molestie lectus placerat non. Fusce luctus gravida leo a dignissim. Aliquam convallis sem et ultricies consectetur. Praesent blandit, odio at vulputate feugiat, elit lacus consequat nisi, a sodales ligula orci porta ipsum. Quisque in diam nibh. Praesent ut dapibus felis. Duis eu quam et diam pulvinar gravida in at felis. Cras odio orci, luctus ac ipsum id, ultrices maximus ex. Nulla faucibus cursus orci, vitae maximus justo. Vivamus quis mauris ut diam pretium venenatis. Donec quis elit consectetur, finibus nisl at, rutrum leo. "
        #To Test server application
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((IP_ADDRESS,4444))

        
        
        self.socketReceiveQueue = Queue(4096)
        self.socketSendQueue = Queue(4096)
        self.serialReceiveQueue = Queue(4096)
        self.serialSendQueue = Queue(4096)
        
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
            #self.com.port = "com22"
            self.com.port = COM_PORT
            self.com.rts = False
            self.com.parity = serial.PARITY_NONE
            self.com.stopbits = serial.STOPBITS_ONE
            self.com.bytesize = 8
            self.com.open()
        except Exception as msg:
            print("SERIAL ERROR: " + str(msg))
            
        if self.com.isOpen():
            print("serial port opened")
        
        TOHandler = threading.Thread(target=self.timeoutHandler)
        TOHandler.start()
        
        
        testHandler = threading.Thread(target=self.testHandlerThread)
        testHandler.start()
        
        serialReceive = threading.Thread(target=self.testSerialReceiveThread)
        serialReceive.start()
        
        
        socketReceive = threading.Thread(target=self.testSocketRecieveThread)
        socketReceive.start()
        
        serialSend = threading.Thread(target=self.testSerialSendThread)
        serialSend.start()
        
        socketSend = threading.Thread(target=self.testSocketSendThread)
        socketSend.start()

        


        
    
    def connect(self, address, portNo):
        self.sock.connect((address, portNo))
        
    
    def startTest(self):
        t1 = threading.Thread(target=self.testSocketSendThread)
        t1.start()
        t3 = threading.Thread(target=self.testHandlerThread)
        t3.start()

    def testSocketRecieveThread(self):
        print("Socket receive thread started")
        while True:
            received = self.sock.recv(4096)
            receivedSTR = received.decode("UTF-8")
            if receivedSTR[0] == '<':
                print("Socket received: "+ receivedSTR)
                self.socketReceiveQueue.put(receivedSTR)
            else:
                print("Socket: Bad data")
#                 receivedSTR.lstrip('<')
#                 receivedSTR.rstrip('>')
#                 receivedSTR = receivedSTR.split("|")
#             
    
    def testSocketSendThread(self):
        print("send thread starting...\n")
        messageNo = 0
        time.sleep(1)
        while True:
            
            sent = self.sock.send(bytes("<" + str(messageNo) +"|" + self.data + ">",'UTF-8'))
            if sent > 0:
                print("Socket send mes no: " + str(messageNo))
                #self.socketSendQueue.put(messageNo)
                #print("add send data to sent list: " + str(messageNo))
                mes = message(messageNo=messageNo,messageBody=self.data)
                self.socketSendList[mes.messageNo] = mes
                messageNo = messageNo + 1
                time.sleep(2)
    
    def testSerialSendThread(self):
        print("serial Send task")
        messageNo = 0
        while True:
            
            dataToSend = bytes("<" + str(messageNo) +"|" + self.data + ">",'UTF-8')
            print("Serial Send: " + str(dataToSend) + "#")
            #self.com.write(dataToSend)
            mes = message(messageNo=messageNo, messageBody=self.data)
            self.com.write(dataToSend)
            self.serialSendList[messageNo] = mes
            #print("in send list: " + self.serialSendList[messageNo].messageBody)
            messageNo = messageNo + 1
            time.sleep(2)
            
            
    def testSerialReceiveThread(self):
        print("serial receive thread started")
        receivedSTR = ""
        unProcessed = ""
        receiving = False
        messageSTR = ""
        state = 0
        while True:
            header = -1
            footer = -1
            recCount = self.com.inWaiting()
            if recCount > 0:
                rec = self.com.read(recCount)
                receivedSTR = rec.decode("UTF-8")
                unProcessed = unProcessed + receivedSTR
                if state == 0:
                    header = unProcessed.find("<")
                    if header != -1:
                        print("header found")
                        state = 1
                        unProcessed = unProcessed[header:]
                if state == 1:
                    
                    footer = unProcessed.find(">")
                    header = unProcessed[1:].find("<")
                    if header != -1:
                        if header < footer:
                            print("HATA: " + str(header) + " " + unProcessed[:header])
                            unProcessed = unProcessed[header:]
                            #log it!
                    if footer != -1:
                        print("footer found")
                        messageSTR = unProcessed[:footer+1]
                        unProcessed = unProcessed[footer:]
                        print("Serial received: " + messageSTR)
                        self.serialReceiveQueue.put(messageSTR)
                        state = 0
                    
        
        
    
    def testHandlerThread(self):
        while True: 
#             if not self.socketSendQueue.empty():
#                 item = self.socketSendQueue.get()
#                 print("item: " + str(item) + " has sent")
#                 self.socketSendList.Append(item)
                
#             if not self.serialSendQueue.empty():
#                 item = self.serialSendQueue.get()
#                 self.serialSendList.Append(item)

            try:
                
                if not self.socketReceiveQueue.empty():
                    #print("Socket Receive Queue received")
                    receivedSTR = self.socketReceiveQueue.get()
                    
                    try:
                        receivedMes = message(data=receivedSTR) 
                        print("received Message No: " + str(receivedMes.messageNo))
                        if self.serialSendList[receivedMes.messageNo].messageBody == self.data:
                            print("Socket Received Message: " + str(receivedMes.messageNo))
                            del self.serialSendList[receivedMes.messageNo]
                        else:
                            print("something wrong")
                            logging.warning("Socket Receive missing message: " + receivedSTR)
                    except Exception as e:
                        print("TH Socket: Bad Data")
                        print(traceback.format_exc())
                        logging.warning("Bad Socket data: " + receivedSTR)
    
                        
                if not self.serialReceiveQueue.empty():
                    receivedSerialSTR = self.serialReceiveQueue.get()
                    try:
                        recMes = message(data = receivedSerialSTR)
                        if self.socketSendList[recMes.messageNo].messageBody == self.data:
                            print("Serial Rec: " + str(recMes.messageNo))
                            del self.socketSendList[recMes.messageNo]
                        else:
                            print("something wrong")
                            logging.warning("msg")
                    except:
                        print("Serial Bad Data")
                        print(traceback.format_exc())
                        logging.warning("Bad Serial Data Arrived: " + receivedSerialSTR)
                
                
    #             if not self.socketReceiveQueue.empty():
    #                 item = self.socketReceiveQueue.get()
    #                 if item[1] != self.data:
    #                     print("error at transmit")
    #                 else:and print("transmit ok")
            except:
                print("An exception occured")
                print(traceback.format_exc())
            pass
        
    def openComport(self):
        pass
    
    def timeoutHandler(self):
        print("Time Out Handler Started")
        while True:
            try:
                for mesNo in list(self.serialSendList.keys()):
                    mes = self.serialSendList[mesNo]
                    if int(time.time() * 1000) - mes.time > 5000:
                        print("Serial Data ERROR")
                        logging.error("Serial: " + str(mesNo))
                        del self.serialSendList[mesNo]
                    
                for mesno in list(self.socketSendList.keys()):
                    mes = self.socketSendList[mesno]
                    if int(time.time() * 1000) - mes.time > 5000:
                        print("Socket data ERROR")
                        logging.error("Socket: " + str(mesno))
                        del self.socketSendList[mesno]
            except KeyError:
                pass
                #print("Pass")
            except:
                print("TO Error: ")
                print(traceback.format_exc())
                
    
ports = list(serial.tools.list_ports.comports())
for p in ports:
    print(p)

print("----------------------------------------------------")


test = tester()
