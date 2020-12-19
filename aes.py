import os
from Crypto.Cipher import AES

class key:

    type_ = "go"
    closed_key = None

    def generate():
        return os.urandom(16)


def encryption(input_text = b"", key = b""):
    output_text = None
    if len(input_text) % 16 == 0:
        output_text = input_text
    else:
        tmp = list(input_text)
        for i in range(16 - (len(input_text) % 16)):
            tmp.append(ord(' '))
            output_text = bytes(tmp)
    aes = AES.new(key, AES.MODE_ECB)
    return aes.encrypt(output_text)


def decryption(encrypted_text = b"", key = b""):
    decrypted_text = None
    if len(encrypted_text) % 16 == 0:
        decrypted_text = encrypted_text
    else:
        tmp = list(encrypted_text)
        for i in range(16 - (len(encrypted_text) % 16)):
            tmp.append(ord(' '))
        decrypted_text = bytes(tmp)
    aes = AES.new(key, AES.MODE_ECB)
    return aes.decrypt(decrypted_text)
