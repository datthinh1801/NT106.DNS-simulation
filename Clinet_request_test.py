import socket
from Message import Message
from MessageHeader import MessageHeader
from MessageQuestion import MessageQuestion
from ParseString import parse_string_msg


msgFromClient = "Hello UDP Server"

bytesToSend = str.encode(msgFromClient)

serverAddressPort = ("127.0.0.1", 20001)

bufferSize = 10000

# Create a UDP socket at client side

UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Send to server using created UDP socket
header = MessageHeader(qr=0,rd=True,ra=True)
question = MessageQuestion("www.facebook.com",qtype=1,qclass=1)
message = Message(header=header,question=question)

message_query_str = str.encode(message.to_string())



UDPClientSocket.sendto(message_query_str, serverAddressPort)

msgFromServer = UDPClientSocket.recvfrom(bufferSize)

msg = "Message from Server {}".format(msgFromServer[0].decode('utf-8'))
print(msg)
UDPClientSocket.close()
message_response_obj = parse_string_msg(msg)
# print("Query question: ",message_response_obj._question.to_string())
# print("Query answer: ")
# for answer in message_response_obj._answer:
#     print(answer.to_string())
