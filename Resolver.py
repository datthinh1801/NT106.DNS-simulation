import socket
import time
from Message import Message
from MessageHeader import MessageHeader
from MessageQuestion import MessageQuestion
from ParseString import parse_string_msg
from ParseString import parse_string_question
from Cache import Cache

class Resolver():
    def __init__(self):
        self.nameservers = []
        #self.timeout = 2.0
        self.Cache = Cache()

    def use_tcp(self, messae:str = None, resolver_ip:str = "127.0.0.1" , resolver_port:int = 10000) -> str :
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

    def use_udp(self, message:str = None, resolver_ip:str = "127.0.0.1" , resolver_port:int = 20001) -> str :
        bytesToSend =  str.encode(message)
        serverAddressPort = (resolver_ip, resolver_port)
        bufferSize = 2048

       # Create a UDP socket at client side
        UDP_Client_Socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        # Send to server using created UDP socket
        UDP_Client_Socket.sendto(bytesToSend, serverAddressPort)
        #receiving data
        data_Response = UDP_Client_Socket.recvfrom(bufferSize)

        #response = data_Respond[0].decode('utf-8')
        response = "Message from Server {}".format(data_Response[0].decode('utf-8'))

        UDP_Client_Socket.close()

        return response    

    def check_qname(self, message:MessageQuestion = None):
        check = message._qname
        len_c = len(check)
        if(check[len_c- 1 ]) != '.':
            new = check + "."
        else:
            new = check
        message._qname = new

    def query(self, message:str = None, tcp=False, source="127.0.0.1", source_port=20001):

        #message_query = parse_string_msg(message)
        #message_question = message_query._question
        message_question = parse_string_question(message)

        self.check_qname(message_question)

        message_info = (message_question._qname, message_question._qtype, message_question._qclass)

        # print(message_info)

        rr = self.Cache.get(message_info)
        if not rr is None:
            print("search in cache")
            return rr 

        header = MessageHeader(qr=0,rd=True,ra=True)
        message = Message(header=header,question=message_question)
        message_query_str = message.to_string()

        #request
        if self.nameservers is None:
            self.nameservers = ['127.0.0.1']

        request = message_query_str
        response = None
        while response is None:
            if tcp:
                response = self.use_tcp(request)
            else:
                response = self.use_udp(request)
            if not response is None:
                break
        
        # print("respones: ",response)
        message_answer = parse_string_msg(response)
        
        #print(response)
        # save to cache
        self.Save_to_Cache(message_answer)
        
        rr = message_answer._answer[0]
        # print("test cache")
        # print((rr[0]._name, rr[0]._type, rr[0]._class))
        # print(self.Cache.get( (rr[0]._name, rr[0]._type, rr[0]._class) ).to_string() )
        # return ResoucrRecord answer
        return rr

    def Save_to_Cache(self, message_reponse:Message = None):
        answers = message_reponse._answer
        authoritys = message_reponse._authority
        additionals = message_reponse._additional

        self.Cache.put( (answers[0]._name, answers[0]._type, answers[0]._class), answers[0])
        """
        # add answer
        for answer in answers:
            self.Cache.put( (answer._name, answer._type, answer._class), answer)
        #add authority
        for authority in authoritys:
            self.Cache.put( (authority._name, authority._type, authority._class), authority )
            
        #add additional
        for additional in additionals:
            self.Cache.put( (additional._name, additional._typy, additional._class), additional )
        """

"""
header = MessageHeader(qr=0,rd=True,ra=True)
domain_resolve = input('Enter a domain name to resolve: ')
question = MessageQuestion(domain_resolve,qtype=1,qclass=1)
mes_question = question.to_string()

#print(message_query_str)
rsv = Resolver()
rr = rsv.query(mes_question,0,"127.0.0.1",20001)
# rr2 = rsv.query(mes_question,0,"127.0.0.1",20001)
#print(type(rr))
print(rr.to_string())
# print(rr2[0].to_string())

#print(question)
print("check in cache")
print(rsv.Cache.get( ("fb.com",1,1) ))
print(rsv.Cache.get( ("fb.com.",1,1)).to_string())
time.sleep(3)

print("search 2nd")
rr2 = rsv.query(mes_question,0,"127.0.0.1",20001)
print(rr2.to_string())
"""
