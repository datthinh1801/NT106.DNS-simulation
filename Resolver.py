import socket
import sys

class Resolver(object):
    def __init__(self, filename='/etc/resolv.conf', configure=True):# tao filename chua nameserver moi
        # init namesaver from my  pc
        self.reset()
        self.read_resolv_conf(filename)

    def reset(self):
        #Reset all resolver configuration to the defaults.
        self.domain = \
            dns.name.Name(dns.name.from_text(socket.gethostname())[1:])
        if len(self.domain) == 0:
            self.domain = dns.name.root
        self.nameservers = []
        self.port = 53
        self.timeout = 2.0
        self.lifetime = 30.0
        self.cache = None


    def read_resolv_conf(self, f):
            # open file default
            if isinstance(f, str) or isinstance(f, unicode):
                try:
                    f = open(f, 'r')
                    # f = open('/etc/resolv.conf', 'r')
                except IOError:
                    # /etc/resolv.conf doesn't exist, can't be read, etc.
                    # We'll just use the default resolver configuration.
                    self.nameservers = ['127.0.0.1']
                    return
                want_close = True
            else:
                want_close = False
            try:
                for l in f:
                    if len(l) == 0 or l[0] == '#' or l[0] == ';':
                        continue
                    tokens = l.split()
                    if len(tokens) == 0:
                        continue
                    if tokens[0] == 'nameserver':
                        self.nameservers.append(tokens[1])
                    elif tokens[0] == 'domain':
                        self.domain = dns.name.from_text(tokens[1])
                    elif tokens[0] == 'search':
                        for suffix in tokens[1:]:
                            self.search.append(dns.name.from_text(suffix))
            finally:
                if want_close:
                    f.close()
            if len(self.nameservers) == 0:
                self.nameservers.append('127.0.0.1')


    def use_tcp(self, message:str = None) -> str :
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('localhost', 10000)
        sock.connect(server_address)

        try:
            # Send data
            byteData = message.encode('utf-8')
            sock.sendall(byteData)
            bufferSize = 2048
            data = sock.recv(bufferSize)
            
            #time out =)))

            # while amount_received < amount_expected:
            #     data = sock.recv(16)
            #     amount_received += len(data)

            # respone = ...
        finally:
            sock.close()
            return respone

    def use_udp(self, message:str = None) -> str :
        bytesToSend = message.encode('utf-8')
        serverAddressPort = ("127.0.0.1", 20001)
        bufferSize = 2048

        # Create a UDP socket at client side
        UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

        # Send to server using created UDP socket
        UDPClientSocket.sendto(bytesToSend, serverAddressPort)
        data_Respond = UDPClientSocket.recvfrom(bufferSize)
        byte_Data = data_Respond[0]
        respone = byte_Data.decode('utf-8')

    def _compute_timeout(self, start):
        now = time.time()
        if now < start:
            if start - now > 1:
                # Time going backwards is bad.  Just give up.
                raise Timeout
            else:
                # Time went backwards, but only a little.  This can
                # happen, e.g. under vmware with older linux kernels.
                # Pretend it didn't happen.
                now = start
        duration = now - start
        if duration >= self.lifetime:
            raise Timeout
        return min(self.lifetime - duration, self.timeout)
    

    def query(self,qname:str = None, qtype:int = 1, qclass=:int = 1, tcp=False, source=None, raise_on_no_answer=True, source_port=0):

"""
            if isinstance(qname, (str, unicode)):
                qname = dns.name.from_text(qname, None)
            if isinstance(rdtype, (str, unicode)):
                rdtype = dns.rdatatype.from_text(rdtype)
            if dns.rdatatype.is_metatype(rdtype):
                raise NoMetaqueries
            if isinstance(rdclass, (str, unicode)):
                rdclass = dns.rdataclass.from_text(rdclass)
            if dns.rdataclass.is_metaclass(rdclass):
                raise NoMetaqueries
"""
            # truong hop qname qtype qclass thoa man
            qnames_to_try = []
            # check duong dan tuyet doi
            if qname.is_absolute():
                qnames_to_try.append(qname)
            
            # else:
            #     if len(qname) > 1:
            #         qnames_to_try.append(qname.concatenate(dns.name.root))
            #     if self.search:
            #         for suffix in self.search:
            #             qnames_to_try.append(qname.concatenate(suffix))
            #     else:
            #         qnames_to_try.append(qname.concatenate(self.domain))
                    
            all_nxdomain = True # not exist domain
            start = time.time()
            for qname in qnames_to_try:
                if self.cache:
                    answer = self.cache.get((qname, qtype, qclass))
                    if not answer is None:
                        if answer.rrset is None and raise_on_no_answer:
                            raise NoAnswer
                        else:
                            return answer
                            # if cache contain ip then return

                request = dns.message.make_query(qname, qtype, qclass)
                # else broadcast nameserver
                
                response = None
                #
                # make a copy of the servers list so we can alter it later.
                #
                nameservers = self.nameservers[:]
                backoff = 0.10
                while response is None:
                    if len(nameservers) == 0:
                        raise NoNameservers
                    for nameserver in nameservers[:]:
                        # set timeout
                        timeout = self._compute_timeout(start)
                        try:
                            if tcp:
                                newmessage = ...
                                # format newmessage from objet to str
                                response = self.use_tcp(newmessage)
                                # response = dns.query.tcp(request, nameserver,
                                #                         timeout, self.port,
                                #                         source=source,
                                #                         source_port=source_port)
                            else:
                                newmessage = ...
                                response =self.use_udp(newmessage)
                                # response = dns.query.udp(request, nameserver,
                                #                         timeout, self.port,
                                #                         source=source,
                                #                         source_port=source_port)
                                if : # co the khong can doan nay =)))
                                    # Response truncated; retry with TCP.
                                    timeout = self._compute_timeout(start)
                                    response = dns.query.tcp(request, nameserver,
                                                        timeout, self.port,
                                                        source=source,
                                                        source_port=source_port)
                        except (socket.error, dns.exception.Timeout):
                            #
                            # Communication failure or timeout.  Go to the
                            # next server
                            #
                            response = None
                            continue

                        except EOFError:
                            # Xảy ra khi hàm input () chạm vào điều kiện end-of-file.
                            
                            # We're using TCP and they hung up on us.
                            # Probably they don't support TCP (though
                            # they're supposed to!).  Take it out of the
                            # mix and continue.
                            #
                            nameservers.remove(nameserver)
                            # delete nameserver
                            response = None
                            continue
                        #
                        # We got a response, but we're not happy with the
                        # rcode in it.  Remove the server from the mix if
                        # the rcode isn't SERVFAIL.
                        #
                        response = None
                    if not response is None:
                        break
                    #
                    # All nameservers failed!
                    #
                    if len(nameservers) > 0:
                        #
                        # But we still have servers to try.  Sleep a bit
                        # so we don't pound them!
                        #
                        timeout = self._compute_timeout(start)
                        sleep_time = min(timeout, backoff)
                        backoff *= 2
                        time.sleep(sleep_time)

                if response.rcode() == dns.rcode.NXDOMAIN:
                    continue
                all_nxdomain = False
                break

            if all_nxdomain:
                raise NXDOMAIN
            answer = Answer(qname, qtype, qclass, response,
                            raise_on_no_answer)
            # save to cache
            if self.cache:
                self.cache.put((qname, qtype, qclass), answer)
            return answer

            


