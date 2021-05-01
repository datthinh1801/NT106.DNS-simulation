import socket
from Message import Message
from MessageHeader import MessageHeader
from MessageQuestion import MessageQuestion
from ParseString import parse_string_msg
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

    def query(self, message:str = None, tcp=False, source="127.0.0.1", source_port=20001):

        message_query = parse_string_msg(message)
        message_question = message_query._question

        rr = self.Cache.get(message_question)
        if not rr is None:
                print("in cache")
                return rr 
        # if cache contain answer -> return else broadcast namesever

        #request
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
        
        #print(response)
        # save to cache
        self.Save_to_Cache(message_answer)
        
        rr = message_answer._answer
        # print("test cache")
        # print((rr[0]._name, rr[0]._type, rr[0]._class))
        # print(self.Cache.get( (rr[0]._name, rr[0]._type, rr[0]._class) ).to_string() )
        # return ResoucrRecord answer
        return rr

    def Save_to_Cache(self, message_reponse:Message = None):
        answers = message_reponse._answer
        authoritys = message_reponse._authority
        additionals = message_reponse._additional

        self.Cache.put((answers[0]._name, answers[0]._type, answers[0]._class), answers[0])
        """
        for answer in answers:
            #print(type(answer))
            print(answer.to_string(), "---save to cache---")
            self.Cache.put( (answer._name, answer._type, answer._class), answer)

            print(self.Cache.get( (answer._name, answer._type, answer._class) ).to_string(), "---print in cache---")
        """
        #add authority
        for authority in authoritys:
            #print(type(authority))
            self.Cache.put( (authority._name, authority._type, authority._class), authority )
            
        #add additional
        for additional in additionals:
            #print(type(additional))
            self.Cache.put( (additional._name, additional._typy, additional._class), additional )

        #print(self.Cache.get((answers[0]._name, answers[0]._type, answers[0]._class)).to_string())



header = MessageHeader(qr=0,rd=True,ra=True)
domain_resolve = input('Enter a domain name to resolve: ')
question = MessageQuestion(domain_resolve,qtype=1,qclass=1)
message = Message(header=header,question=question)
message_query_str = message.to_string()

#print(message_query_str)
rsv = Resolver()
rr = rsv.query(message_query_str,0,"127.0.0.1",20001)
#print(type(rr))
print(rr[0].to_string())

#print(question)
print(rsv.Cache.get( ("fb.com",1,1) ))
print(rsv.Cache.get( ("fb.com.",1,1)).to_string())
