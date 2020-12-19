import os

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
import base64
import math


class key:
    type_ = "go"  # "go" = generate once; "gps" = generate every time before send

    def generate():
        key = RSA.generate(2048, os.urandom)
        private_bytes = key.export_key()
        with open(f"private.pem", "wb") as f:
            f.write(private_bytes)
        public_bytes = key.publickey().export_key()
        #with open(f"public.pem", "wb") as f:
        #    f.write(public_bytes)
        return public_bytes


chunk_encrypt_size = 200
chunk_decrypt_size = 256


def encryption(input_text=b"", key=b""):  # Here we will send signature + input_text
    public_key = RSA.import_key(key)
    cipher_rsa = PKCS1_OAEP.new(public_key)
    text_length = len(input_text)
    print(f"text length {text_length}")

    chunks_count = math.ceil(text_length / chunk_encrypt_size)
    print(f"encrypting as {chunks_count} chunks")
    result = b""
    for i in range(chunks_count):
        chunk = input_text[chunk_encrypt_size * i:chunk_encrypt_size * (i + 1)]
        result += cipher_rsa.encrypt(chunk)
    return result


def decryption(encrypted_text=b"", key=b""):
    if len(encrypted_text) % 256 == 0:
        added_text = encrypted_text
    else:
        tmp = list(encrypted_text)
        for i in range(256 - (len(encrypted_text) % 256)): #if not enough symbols, adds b' '
            tmp.append(ord(' '))
            added_text = bytes(tmp)
    #if enc_length % 256 > 0:
    #    raise ValueError("len of encrypted text not divides by 256")
    enc_length = len(encrypted_text)

    key_bytes = open(f"private.pem", 'rb').read()
    private_key = RSA.import_key(key_bytes)
    cipher_rsa = PKCS1_OAEP.new(private_key)
    chunks = int(enc_length / chunk_decrypt_size)
    print(f"decrypting {chunks} chunks")
    result = b""
    for i in range(chunks):
        chunk = added_text[chunk_decrypt_size * i:chunk_decrypt_size * (i + 1)]
        try:
            result += cipher_rsa.decrypt(chunk)
        except ValueError:
            pass
    return result


def test():
    public = key().generate()
    text = "my passphrase" * 1000
    encrypted_text = encryption(text.encode("utf8"), key=public)
    print(f"encrypted len {len(encrypted_text)}")
    print(f"encrypted is {base64.b64encode(encrypted_text)}")
    decrypted_text = decryption(encrypted_text)
    print(f"decrypted is {decrypted_text}")
    print(f"test passed? {text == decrypted_text}")


if __name__ == '__main__':
    test()
