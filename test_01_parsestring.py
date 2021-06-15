from Message import Message
from MessageHeader import MessageHeader
from MessageQuestion import MessageQuestion
from ResourceRecord import ResourceRecord
from ParseString import *


def test_parse_header():
    header = MessageHeader()
    plain_header = header.to_string()

    # reconstruct the header
    lines = plain_header.splitlines()
    header_id = lines[0]
    header_flags = lines[1]
    header_qdcount = int(lines[2])
    header_ancount = int(lines[3])
    header_nscount = int(lines[4])
    header_arcount = int(lines[5])
    flags = parse_string_flag(header_flags)
    print(flags)
    parsed_header = MessageHeader(id=int(header_id),
                                  qr=flags['qr'],
                                  opcode=flags['opcode'],
                                  aa=flags['aa'],
                                  tc=flags['tc'],
                                  rd=flags['rd'],
                                  ra=flags['ra'],
                                  rcode=flags['rcode'])
    assert plain_header == parsed_header.to_string()


def test_parse_question():
    question = MessageQuestion('www.google.com', 1, 1)
    plain_question = question.to_string()
    parsed_question = parse_string_question(plain_question)
    assert plain_question == parsed_question.to_string()


def test_parse_resourcerecord():
    rr = ResourceRecord('www.google.com', 1, 1, 100, '127.0.0.1')
    plain_rr = rr.to_string()
    parsed_rr = parse_string_resource_record(plain_rr)
    assert plain_rr == parsed_rr.to_string()


def test_parse_string_msg():
    header = MessageHeader()
    question = MessageQuestion('www.google.com', 1, 1)
    message = Message(header=header, question=question)
    plain_message = message.to_string()
    parsed_message = parse_string_msg(plain_message)
    assert plain_message == parsed_message.to_string()
