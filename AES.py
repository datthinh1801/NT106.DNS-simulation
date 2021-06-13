from Crypto import Random
from Crypto.Cipher import AES
import base64
import hashlib


class AESCipher:
    def __init__(self):
        """
        initiale AES encryption with hard code key and initial vector
        """

        self.block_size = AES.block_size
        self.key_str = 'NT106.ANTN2019-NHOM-1'

        # sha256 to return 256 key, set AES256
        self.key = hashlib.sha256(self.key_str.encode()).digest()

        # initial vector 16 bytes length
        self.iv = b'ANTN2019ANTN2019'

    def encrypt(self, plain):
        """
        AES 256 encrypt string encode to base64 the return in bytes type
        """

        plain = self.padding(plain)
        encryption = AES.new(self.key, AES.MODE_CBC, self.iv)
        return base64.b64encode(encryption.encrypt(plain.encode()))

    def decrypt(self, cipher):
        """
        AES 256 decrypt return turn a recovered string
        """

        cipher = base64.b64decode(cipher)
        decryption = AES.new(self.key, AES.MODE_CBC, self.iv)
        return self.unpadding(decryption.decrypt(cipher)).decode('utf-8')

    def padding(self, msg):
        """
        Padding at the end msg
        """
        return msg + (self.block_size - len(msg) % self.block_size)*chr(self.block_size-len(msg) % self.block_size)

    @staticmethod
    def unpadding(msg):
        """
        Unpadding the msg with the padding algorithm
        """
        return msg[:-ord(msg[len(msg)-1:])]
