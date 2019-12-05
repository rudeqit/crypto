#!/usr/bin/env python3

### Add path to operations lib 
import os
import sys
sys.path.append("..")

from operations.operations import get_rand

LOG = True

class Vernama:

    def __init__(self, file_in):
        self.get_keys(file_in)
        self.alice = Subscriber(self.keys)
        self.bob = Subscriber(self.keys)
        self.write_keys_in_file()
    
    def get_keys(self, file_in):
        self.keys = []
        size_file = os.path.getsize(file_in)

        for any_byte in range(0, size_file + 1):

            key = get_rand()
            self.keys.append(key)

    def vernama(self, file_in, file_out):
        ### Log shit
        enc = []

        index = 0

        with open(file_in, "rb") as fd_in, open(file_out, "wb") as fd_out:

            while True:
                ### Read file byte to byte
                num_bytes = 1 
                element = fd_in.read(num_bytes)
                if not element:
                    break
                
                el = int.from_bytes(element, byteorder="little")
                index += 1
                alice_encode = self.alice.encode(el, index)
                bob_decode = self.bob.decode(alice_encode, index)

                ### Should be equal
                # print(el)
                # print(bob_decode)

                if LOG:
                    enc.append(f"{alice_encode}\n")

                ### Write decode info in file
                fd_out.write(bob_decode.to_bytes(num_bytes, byteorder="little"))
        
        if LOG:
            self.log(enc)

        print(f"Hello from Vernam cipher!")
        print(f"Alice encode file \'{file_in}\' and send it to Bob.")
        print(f"Bob recv msg, decode and save it in \'{file_out}\'.")


    def write_keys_in_file(self, vernam_keys="vernam_keys"):
        with open(vernam_keys, "w") as fd:

            for elem in self.keys:
                fd.write(f"{elem}\n")

    def log(self, encode, rsa_encode = "vernam_encode"):
        with open(rsa_encode, "w") as fd_en:
            
            for elem in encode:
                fd_en.write(elem)


class Subscriber:
    
    def __init__(self, keys):
        self.keys = keys

    def encode(self, message, index) -> tuple:
        return message ^ self.keys[index]

    def decode(self, encode, index):
        return encode ^ self.keys[index]

if __name__ == "__main__":
    # file_in, file_out = "pic.jpg", "out_pic.jpg"
    file_in, file_out = "1.txt", "2.txt"     

    cipers_vernama = Vernama(file_in)
    cipers_vernama.vernama(file_in, file_out)