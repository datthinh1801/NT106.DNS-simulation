import socket
import sys
import constant
from Message import Message
from MessageHeader import MessageHeader
from MessageQuestion import MessageQuestion
from ParseString import parse_string_msg

class Resolver:
    def __init__(self):
        self.nameservers = []
        #self.timeout = 2.0
        self.cache = None

    def use_tcp(self, message:str = None, resolver_ip:str = RESOLVER_IP , resolver_port:int = RESOLVER_PORT) -> str :
        # Create a TCP socket at client side
        TCPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (resolver_ip, resolver_port)
        TCPClientSocket.connect(server_address)

        try:
            # Sending data
            bytesToSend = message.encode('utf-8')
            TCPClientSocket.sendall(bytesToSend)

            #bufferSize = 2048 trong constant

            #receiving data
            data_Respond = TCPClientSocket.recv(bufferSize)
            response = data_Respond.decode('utf-8')
        finally:
            TCPClientSocket.close()
            return response

    def use_udp(self, message:str = None, resolver_ip:str = RESOLVER_IP , resolver_port:int = RESOLVER_PORT) -> str :
        bytesToSend = message.encode('utf-8')
        serverAddressPort = (resolver_ip, resolver_port)
        bufferSize = 2048

       # Create a UDP socket at client side
        UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        try:
        # Send to server using created UDP socket
        UDPClientSocket.sendto(bytesToSend, serverAddressPort)

        #receiving data
        data_Respond = UDPClientSocket.recvfrom(bufferSize)
        response = data_Respond.decode('utf-8')
        finally:
            TCPClientSocket.close()
            return response    

    def query(self, message:str = None, tcp=False, source=None, source_port=0):

        message_query = parse_string_msg(message)
        message_question = message.question

        if self.cache:
            rr = self.cache.get(question)
            if not rr is None:
                    return rr 
        # if cache contain answer -> return else broadcast namesever

        #request:Message = ....
        if self.nameservers is None:
            self.nameservers = ['127.0.0.1']

        request = message
        response = None
        while response is None:
            if tcp:
                response = self.use_tcp(request)
            else:
                response = self.use_udp(request)

            if not response is None:
                break
        

        message_answer = parse_string_msg(response)
            
        # save to cache
        Save_to_Cache(message_answer)
        
        rr = message_answer._answer
        # return ResoucrRecord answer
        return rr

    def Save_to_Cache(self, message_reponse:Message = None):
        answer = message_reponse._answer
        authority = message_reponse._authority
        additional = message_reponse._additional

        # add answer
        self.cache.put((answer._name, answer._type, answer._class), answer)

        #add authority
        for i in authority:
            self.cache.put( (i._name, i._type, i._class), i )
            
        #add additional
        self.cache.put( (additional._name, additional._typy, additional._class), additional )
