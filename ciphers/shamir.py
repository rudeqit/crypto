#!/usr/bin/env python3

### Add path to operations lib 
import sys
sys.path.append("..")

from operations.operations import pow_mod, get_rand_simple, get_rand, steroid_evklid

LOG = True

class Shamir:

    def __init__(self, p = None):
        self.p = get_rand_simple() if p is None else p

        ### Init two subscribers - Alice and Bob
        self.alice = Subscriber(self.p)
        self.bob = Subscriber(self.p)

    def shamir(self, file_in, file_out):
        ### Log shit
        xxx = []
        xxx_enc = []

        with open(file_in, "rb") as fd_in, open(file_out, "wb") as fd_out:
            while True:
                ### Read file byte to byte
                num_bytes = 1 
                element = fd_in.read(num_bytes)
                if not element:
                    break
                
                el = int.from_bytes(element, byteorder="little")
                
                x1 = self.alice.encode(el)
                x2 = self.bob.encode(x1)
                x3 = self.alice.decode(x2)
                x4 = self.bob.decode(x3)

                ### Should be equal
                # print(el)
                # print(x4)

                if LOG:
                    xxx.append(f"{el} --> {x1} --> {x2} --> {x3} --> {x4}\n")
                    xxx_enc.append(f"{x1} --> {x2} --> {x3}\n")
                
                ### Write decode info in file
                fd_out.write(x4.to_bytes(num_bytes, byteorder="little"))

        if LOG:
            self.log(xxx, xxx_enc)

        print(f"Hello from Shamir cipher!")
        print(f"Alice encode file \'{file_in}\' and send it to Bob.")
        print(f"Bob recv msg, decode and save it in \'{file_out}\'.")

    
    def log(self, xxx, xxx_enc, keys_file = "shamir_keys", encode_file = "shamir_encode"):
        with open(keys_file, "w") as fd_kf, open(encode_file, "w") as fd_ef:
            
            fd_kf.write(f"p = {self.p}, ca = {self.alice.c}, da = {self.alice.d}, cb = {self.bob.c}, db = {self.bob.d}\n")
            
            for x in xxx:
                fd_kf.write(x)

            for x in xxx_enc:
                fd_ef.write(x)

            

class Subscriber:

    def __init__(self, p):
        self.p = p
        self.get_param(self.p)

    def encode(self, message):
        return pow_mod(message, self.c, self.p)

    def decode(self, message):
        return pow_mod(message, self.d, self.p)

    def get_param(self, p):
        self.c = get_rand() % (p - 1)               
        nod, x, y = steroid_evklid(p - 1, self.c)

        while nod != 1 or y <= 0:
            self.c = get_rand() % (p - 1)  
            nod, x, y = steroid_evklid(p - 1, self.c)
        self.d = y

        # temp = (self.c * self.d) % (p - 1)
        # print(f"self.c * self.d % p - 1 = {temp}")



if __name__ == "__main__":    
    # file_in, file_out = "pic.jpg", "out_pic.jpg"
    file_in, file_out = "1.txt", "2.txt"   

    cipers_shamir = Shamir()
    cipers_shamir.shamir(file_in, file_out)