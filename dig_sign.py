#We use here digital signature
import os
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15


class key:
    
    type_ = "go" # "go" = generate once; "gps" = generate every time before send

    def generate():
        private_key = RSA.generate(1024, os.urandom)
        public_key = private_key.publickey()
        with open('key.pem', 'wb') as f:
            f.write(private_key.export_key("PEM"))
        return public_key.export_key("PEM")

def encryption(input_text = b"", key = b""): #Here we will send signature + input_text
    private_key = None
    with open('key.pem', 'rb') as f:
        private_key = RSA.import_key(f.read())
    h = SHA256.new()
    h.update(input_text)
    sign = pkcs1_15.new(private_key).sign(h) #len(sign) = 128
    print("I'm reached to encryption!")
    return sign + input_text

def decryption(encrypted_text = b"", key = b""): #
    public_key = RSA.import_key(key)
    sign = encrypted_text[:128]
    h = SHA256.new()
    h.update(encrypted_text[128:])
    try:
        pkcs1_15.new(public_key).verify(h, sign)
        return encrypted_text[128:]
    except (ValueError, TypeError):
        return b"The signature is not valid!\n" + encrypted_text[128:]

