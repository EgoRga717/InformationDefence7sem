#We use here symmetric encryption, DES
import os
from Crypto.Cipher import DES

class key:
    
    type_ = "go" # "go" = generate once; "gps" = generate every time before send
    closed_key = None

    def generate():
        return os.urandom(8)

def encryption(input_text = b"", key = b""):
    output_text = None
    if len(input_text) % 8 == 0:
        output_text = input_text
    else:
        #Need for correctly encryption
        tmp = list(input_text)
        for i in range(8 - (len(input_text) % 8)): #if not enough symbols, adds b' '
            tmp.append(ord(' '))
            output_text = bytes(tmp)
    des = DES.new(key, DES.MODE_ECB)
    return des.encrypt(output_text)

def decryption(encrypted_text = b"", key = b""):
    decrypted_text = None
    if len(encrypted_text) % 8 == 0:
        decrypted_text = encrypted_text
    else:
        #if we here, then it means that something was added/deleted
        tmp = list(encrypted_text)
        for i in range(8 - (len(encrypted_text) % 8)): #if not enough symbols, adds b' '
            tmp.append(ord(' '))
        decrypted_text = bytes(tmp)
    des = DES.new(key, DES.MODE_ECB)
    return des.decrypt(decrypted_text)

