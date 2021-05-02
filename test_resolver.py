import socket
import time
from Resolver import Resolver
from Message import Message
from MessageHeader import MessageHeader
from MessageQuestion import MessageQuestion
from ParseString import parse_string_msg
from ParseString import parse_string_question
from Cache import Cache


rsv = Resolver()

header = MessageHeader(qr=0,rd=True,ra=True)
domain_resolve = input('Enter a domain name to resolve: ')
question = MessageQuestion(domain_resolve,qtype=1,qclass=1)
mes_question = question.to_string()

rr = rsv.query(mes_question,0,"127.0.0.1",20001)
print("-- answer: ")
print(rr.to_string())
print("-- check in cache --")
print(rsv.Cache.get( ("fb.com",1,1) ))
print(rsv.Cache.get( ("fb.com.",1,1)).to_string())
time.sleep(3)

print("-- search 2nd --")
rr2 = rsv.query(mes_question,0,"127.0.0.1",20001)
print(rr2.to_string())
