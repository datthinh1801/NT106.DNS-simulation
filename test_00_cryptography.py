from AES import *
from Message import Message
from MessageHeader import MessageHeader
from MessageQuestion import MessageQuestion


def test_basic_crypto_functions():
    message = "AES symmetric cryptography"
    ciphertext = AESCipher().encrypt(message)
    recovered_text = AESCipher().decrypt(ciphertext)
    assert message == recovered_text


def test_crypto_functions_on_message():
    header = MessageHeader()
    question = MessageQuestion('www.google.com', 1, 1)
    message = Message(header=header, question=question)
    plain_message = message.to_string()
    ciphertext = AESCipher().encrypt(plain_message)
    recovered_text = AESCipher().decrypt(ciphertext)
    assert recovered_text == plain_message
