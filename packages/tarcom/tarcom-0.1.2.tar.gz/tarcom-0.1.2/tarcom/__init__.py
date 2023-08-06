# Programmer: Tarek Darghouth Moghrabi
# Created: 2019, 4, 24, 18: 13

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files(the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and / or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


import os
import time
import threading
import socket
import asyncore

# NetworkCom: Tcp server and client.


class NetworkCom:

    @property
    def networkType(self):
        return self.__networkType

    @networkType.setter
    def networkType(self, value):
        self.__networkType = value

    @property
    def connected(self):
        return self.__connected

    @connected.setter
    def connected(self, value):
        self.__connected = value

    @property
    def address(self):
        return self.__address

    @address.setter
    def address(self, value):
        self.__address = value

    @property
    def name(self):
        return self.__name

    @property
    def ipLocal(self):
        return self.__ipLocal

    @property
    def port(self):
        return self.__port

    @port.setter
    def port(self, value):
        self.__port = value

    @property
    def connectionUpdated(self):
        return self.__connectionUpdated

    @connectionUpdated.setter
    def connectionUpdated(self, value):
        self.__connectionUpdated.removeAt(0)
        self.__connectionUpdated.append(value)

    @property
    def dataReceived(self):
        return self.__dataReceived

    @dataReceived.setter
    def dataReceived(self, value):
        self.__dataReceived.removeAt(0)
        self.__dataReceived.append(value)

    @property
    def dataCurrent(self):
        return self.__dataCurrent

    __networkType = 0
    __connected = False
    __address = None
    __name = None
    __ipLocal = None
    __dataCurrent = None
    __tcp = None

    def __init__(self, networkType, port, address=None):
        self.__networkType = networkType

        if port < 0 or networkType > 1:
            raise Exception(
                "Network type should be [0] for server or [1] for client.")

        self.__connected = False
        self.__address = address
        self.__ipLocal = NetworkCom.getLocalIP(address)

        if self.__networkType == 0 and address != None:
            self.__ipLocal = address

        if self.__address == None:
            self.__address = ""

        if port > 65535:
            raise Exception("Port should be smaller than 65535.")
        if port <= 0:
            raise Exception("Port should be bigger than 0.")

        self.__port = port
        self.checkConnect()

        self.__connectionUpdated = Event()
        self.__connectionUpdated()
        self.__dataReceived = Event()
        self.__dataReceived()

    @staticmethod
    def getLocalIP(address):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect((address, 1))
            IP = s.getsockname()[0]
        except:
            try:
                s.connect(('10.255.255.255', 1))
                IP = s.getsockname()[0]
            except:
                IP = ''
        finally:
            s.close()
        return IP

    def connectionUpdatedHandler(self, args):
        if self.__networkType == 0:
            self.connected = args.connected
            self.connectionUpdated(self, args)
        elif self.__networkType == 1:
            if self.connected != args.connected:
                self.connected = args.connected
                self.connectionUpdated(self, args)

    def dataReceivedHandler(self, args):
        self.__dataCurrent = args.data
        self.__dataReceived(self, args)

    def connect(self):
        self.__tcp = AsyncoreSocketTCP(
            self.networkType, self.__ipLocal, self.__address, self.__port)
        self.__tcp.isCheck = True
        self.__tcp._connUpdatedEvent.append(self.connectionUpdatedHandler)
        self.__tcp._dataRcvEvent.append(self.dataReceivedHandler)

        self.checkConnect()
        loop_thread = threading.Thread(
            target=asyncore.loop, name="Asyncore Socket Loop " + self.__address + ":" + str(self.__port))
        loop_thread.daemon = True
        loop_thread.start()

    def checkConnect(self):
        pass

    def send(self, msg):
        self.__tcp.send(msg)

    def close(self):
        self.connected = False
        self.__tcp.close()


class AsyncoreSocketTCP(asyncore.dispatcher_with_send):

    _connUpdatedEvent = None
    _dataRcvEvent = None

    __connected = False
    __ipLocal = None
    __ipRemote = None
    __sockets = None
    __port = -1
    __data = None
    __isCheck = False
    __networkType = 0
    __checkCount = 0
    __checkCountMax = 15
    __clientReadThreads = None
    __isClosed = False

    def __init__(self, networkType, ipLocal, ipRemote, port):
        self.__ipRemote = list()
        self.__sockets = list()
        self.__clientReadThreads = list()

        self.__networkType = networkType
        self.__ipLocal = ipLocal
        if os.name != "nt":
            self.__ipLocal = ''
        if networkType == 1 and ipRemote != None:
            self.validateIp(ipRemote)
            self.__ipRemote.append(ipRemote)
        self.__port = port

        self._connUpdatedEvent = Event()
        self._connUpdatedEvent()
        self._dataRcvEvent = Event()
        self._dataRcvEvent()

        asyncore.dispatcher.__init__(self)
        self.startConnect()

    def validateIp(self, ip):
        try:
            socket.inet_aton(ip)
        except socket.error:
            raise Exception("Invalid ip " + ip)

    def startConnect(self):
        if self.__isClosed:
            pass

        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        if self.__networkType == 0:
            self.bind((self.__ipLocal, self.__port))
            self.listen(10)
        elif self.__networkType == 1:
            try:
                self.connect((self.__ipRemote[0], self.__port))
                pass
            except Exception as e:
                if e != None:
                    pass
                time.sleep(1)
                self.startConnect()
                pass

    def handle_connect_event(self):
        asyncore.dispatcher_with_send.handle_connect_event(self)
        if self.connected:
            self.__connected = True
            self._connUpdatedEvent(
                ConnectionUpdatedEventArgs(self.__ipRemote[0], True))

    def handle_accepted(self, sock, addr):
        if self.__ipRemote.__contains__(addr[0]):
            self.__ipRemote.remove(addr[0])
            for socket in self.__sockets:
                if socket[0] == addr[0]:
                    self.__sockets.remove(socket)
                    break
            for clientReadThread in self.__clientReadThreads:
                if clientReadThread[0] == addr[0]:
                    clientReadThread[1].isClose = True
                    self.__clientReadThreads.remove(clientReadThread)
                    break

        self.__ipRemote.append(addr[0])
        self.__sockets.append((addr[0], sock))
        thread = threading.Thread(target=self.readData, name="Client Read Loop " +
                                  addr[0] + ":" + str(self.__port), args=[addr[0], sock, True])
        thread.daemon = True
        thread.start()
        self.__clientReadThreads.append((addr[0], thread))
        self._connUpdatedEvent(ConnectionUpdatedEventArgs(addr[0], True))

    def handle_error(self):
        pass

    def handle_expt(self):
        pass

    def handle_close(self):
        pass

    def handle_read(self):
        if self.__isCheck:
            self.__checkCount += 1
            if self.__checkCount >= self.__checkCountMax:
                self.__checkCount = 0
                if self.__connected:
                    if self.__networkType == 1:
                        self.connected = False
                        self.__connected = False
                        self._connUpdatedEvent(
                            ConnectionUpdatedEventArgs(self.__ipRemote[0], False))
                        try:
                            self.connected = False
                            self.__connected = False
                            for ip in self.__ipRemote:
                                self._connUpdatedEvent(
                                    ConnectionUpdatedEventArgs(ip, False))
                            self.socket.close()
                            asyncore.dispatcher_with_send.close(self)
                        except Exception as e:
                            if e != None:
                                pass
                        while not self.socket.__closed:
                            pass
                        time.sleep(1)
                        self.startConnect()

        self.readData(self.__ipRemote[0], self.socket)

    def readData(self, remoteAddress, socket, always=False):
        address = remoteAddress
        while(True):
            try:
                data, addr = socket.recvfrom(65000)
                dataCount = len(data)
                if dataCount > 0:
                    if self.__networkType == 1:
                        if not self.__connected:
                            self.__connected = True
                            self._connUpdatedEvent(
                                ConnectionUpdatedEventArgs(address, True))
                    self.__checkCount = 0
                    self.__data = data
                    self._dataRcvEvent(DataReceivedEventArgs(
                        address, data.decode('utf-8')))
                else:
                    if self.__isCheck:
                        self.__checkCount += 1
                        if self.__checkCount >= self.__checkCountMax:
                            self.__checkCount = 0
                            if self.__networkType == 0:
                                self._connUpdatedEvent(
                                    ConnectionUpdatedEventArgs(address, False))
                                break
            except Exception as e:
                if e != None:
                    pass
                if self.__networkType == 0:
                    self.__checkCount = 0
                pass
            if not always:
                break
            else:
                t = threading.currentThread()
                isClose = getattr(t, "isClose", False)
                if isClose:
                    break

    def writable(self):
        return True

    def readable(self):
        return True

    def send(self, msg, ip=None):
        sendIp = list()
        if ip != None:
            sendIp.append(ip)
        else:
            sendIp = self.__ipRemote
        for ip in sendIp:
            if ip != None:
                try:
                    if self.__networkType == 0:
                        for socket in self.__sockets:
                            if socket[0] == ip:
                                socket[1].send(bytes(msg, 'utf-8'))
                                break
                    elif self.__networkType == 1:
                        self.socket.sendto(
                            bytes(msg, 'utf-8'), (ip, self.__port))
                except Exception as e:
                    if e != None:
                        pass
                    pass

    def close(self):
        if not self.__isClosed:
            self.__isClosed = True
            self.connected = False
            self.__connected = False
            for ip in self.__ipRemote:
                self._connUpdatedEvent(ConnectionUpdatedEventArgs(ip, False))
            asyncore.dispatcher_with_send.close(self)


class Event(list):
    def __call__(self, *args, **kwargs):
        for f in self:
            f(*args, **kwargs)

    def __repr__(self):
        return "Event(%s)" % list.__repr__(self)

    def removeAt(self, index):
        if index < len(self):
            self.remove(self[index])


class ConnectionUpdatedEventArgs:
    @property
    def address(self):
        return self.__address

    @property
    def connected(self):
        return self.__connected

    __address = None
    __connected = None

    def __init__(self, address, connected):
        self.__address = address
        self.__connected = connected


class DataReceivedEventArgs:
    @property
    def address(self):
        return self.__address

    @property
    def data(self):
        return self.__data

    __address = None
    __data = None

    def __init__(self, address, data):
        self.__address = address
        self.__data = data


class TcpServer(NetworkCom):
    def __init__(self, port, address=None):
        super().__init__(0, port, address)


class TcpClient(NetworkCom):
    def __init__(self, address, port):
        super().__init__(1, port, address)
