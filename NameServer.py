from Message import Message
import socket 
def ParseTextToMessage(str_query: str):

# Nameserver class definition
class NameServer:
    def __init__(self,Cache: bool = False):
        """
        Receive the query from resolver in raw text format and Parse raw text to Messages Object 
        to handle the query then send respone or continously send query to other zonr( recursive-query)
        """
        #self.__Zone = None
        self.__Cache = Cache
    def Query_handle(self, qname: str = None, qtype: int = None, qclass: int = None, socket=  None) -> Message: 


    def start_listening_TCP(self):
        # Create a TCP socket
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        server_address = ('localhost', 10000)
        buffersize = 2048

        # Bind the socket to the port
        sock.bind(server_address)

        #listen for incomming connections
        sock.listen(1)
        while True:
            #wait for a connection 
            connection,client_address = sock.accept()
            try:
                byteData = connection.recv(buffersize)
                data = byteData.decode('utf-8')
                if data:
                    message_query = ParseTextToMessage(data)
                    #Query_handle(message_query.getter....  # code more after has respone
                else:
                    break  ##### code more to print out error
            finally:
                connection.close()
    def start_listening_UDP(self):
        # create a UDP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_address = ('localhost', 20001)
        buffersize = 2048

        # bind the socket to the port
        sock.bind(server_address)

        while True:
            byteData = sock.recv(buffersize)
            data = byteData.decode('utf-8')

            # Query_handle


    def Send_Respone(self):