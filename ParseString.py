from Message import Message
from MessageQuestion import MessageQuestion
from MessageHeader import MessageHeader
from ResourceRecord import ResourceRecord


def parse_string_flag(flags: str) -> dict:
    """Parse a hex string of flags to a dictionary of flags with values converted properly."""
    # convert hex string to bin string
    bin_str = bin(int(flags, 16))[2:]

    d_flags = dict()
    cur_bit_pos = 0

    # get 1-bit QR
    d_flags['qr'] = int(bin_str[cur_bit_pos])
    cur_bit_pos += 1

    # get 4-bit OPCODE
    d_flags['opcode'] = int(bin_str[cur_bit_pos: cur_bit_pos + 4], 2)
    cur_bit_pos += 4

    # get 1-bit AA
    d_flags['aa'] = bool(bin_str[cur_bit_pos])
    cur_bit_pos += 1

    # get 1-bit TC
    d_flags['tc'] = bool(bin_str[cur_bit_pos])
    cur_bit_pos += 1

    # get 1-bit RD
    d_flags['rd'] = bool(bin_str[cur_bit_pos])
    cur_bit_pos += 1

    # get 1-bit RA
    d_flags['ra'] = bool(bin_str[cur_bit_pos])
    cur_bit_pos += 1

    # get 3-bit Z
    d_flags['z'] = int(bin_str[cur_bit_pos: cur_bit_pos + 3], 2)
    cur_bit_pos += 3

    # get 4-bit RCODE
    d_flags['rcode'] = int(bin_str[cur_bit_pos: cur_bit_pos + 4], 2)

    return d_flags


def parse_string_question(question: str) -> MessageQuestion:
    """Parse a question string to a MessageQuestion object."""
    fields = question.split(';')
    qname = fields[0]
    qtype = int(fields[1])
    qclass = int(fields[2])
    return MessageQuestion(qname, qtype, qclass)


def parse_string_resource_record(rr: str) -> ResourceRecord:
    """Parse a resource record string to a ResourceRecord object."""
    fields = rr.split(';')
    _name = fields[0]
    _type = int(fields[1])
    _class = int(fields[2])
    _ttl = int(fields[3])
    _rdata = fields[4]
    return ResourceRecord(_name, _type, _class, _ttl, _rdata)


def parse_string_msg(msg: str) -> Message:
    """Parse a message string to a Message object."""
    lines = msg.splitlines()

    # [header]
    header_id = lines[0]
    header_flags = lines[1]
    header_qdcount = int(lines[2])
    header_ancount = int(lines[3])
    header_nscount = int(lines[4])
    header_arcount = int(lines[5])

    # parse flags
    flags = parse_string_flag(header_flags)

    # create a MessageHeader object
    header = MessageHeader(id=header_id,
                           qr=flags['qr'],
                           opcode=flags['opcode'],
                           aa=flags['aa'],
                           tc=flags['tc'],
                           rd=flags['rd'],
                           ra=flags['ra'],
                           rcode=flags['rcode'])

    # [body]
    # question
    question_str = lines[6]
    question = parse_string_question(question_str)

    # tracker
    cur_line = 7

    # Create the Message object
    message = Message(header=header, question=question)

    # [KNOWN ERROR]
    # If the message is truncated, the counts will decline automatically
    # (via the _set_header_flags_automatically() method in Message class)

    # answers
    ans = []
    for _ in range(header_ancount):
        ans.append(parse_string_resource_record(lines[cur_line]))
        cur_line += 1
    message.add_records_to_answer_section(ans)

    # authority
    nss = []
    for _ in range(header_nscount):
        nss.append(parse_string_resource_record(lines[cur_line]))
        cur_line += 1
    message.add_records_to_authority_section(nss)

    # additional
    ads = []
    for _ in range(header_arcount):
        ads.append(parse_string_resource_record(lines[cur_line]))
        cur_line += 1
    message.add_records_to_additional_section(ads)

    return message
