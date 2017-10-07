class EmailServer:
    def __init__(self, name, host, port, protocol):
        self.__name = name
        self.__host = host
        self.__port = port
        self.__protocol = protocol

    def getName(self):
        return self.__name

    def setName(self, name):
        self.__name = name

    def getHost(self):
        return self.__host

    def setHost(self, host):
        self.__host = host

    def getPort(self):
        return self.__port

    def setPort(self, port):
        self.__port = port

    def getProtocol(self):
        return self.__protocol

    def setProtocol(self, protocol):
        self.__protocol = protocol