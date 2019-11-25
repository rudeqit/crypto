#!/usr/bin/env python3

### Add path to operations lib 
import sys
sys.path.append("../operations")

from operations import diff_hell, pow_mod, get_rand_simple, get_rand, steroid_evklid

class Shamir:
    def __init__(self, p = None):
        self.p = get_rand_simple() if p is None else p
        ### Init two subscribers - Alice and Bob
        self.alice = Subscriber(self.p)
        self.bob = Subscriber(self.p)

    def shamir(self, file_in, file_out):
        with open(file_in, "rb") as fd_in, open(file_out, "wb") as fd_out:
            while True:
                ### Read file byte to byte
                num_bytes = 1 
                element = fd_in.read(num_bytes)
                if not element:
                    break
                
                el = int.from_bytes(element, byteorder="little")
                
                x1 = self.alice.encode(el)
                x2 = self.bob.encode(el)
                x3 = self.alice.decode(el)
                x4 = self.bob.decode(el)
                
                ### Write decode info in file
                # self.log(x1, x2, x3)
                fd_out.write(x4.to_bytes(num_bytes, byteorder="little"))

    def log(self, x1, x2, x3, keys_file = "Shamir_Keys.txt", decode_value = "Shamir_Decode.txt"):
        with open(keys_file, "a") as fd_kf, open(decode_value, "a") as fd_df:
            fd_kf.write(f"p = {self.p}, ca = {self.alice.c}, da = {self.alice.d}, cb = {self.bob.c}, db = {self.bob.d}\n")
            fd_df.write(f"x1 = {x1}, x2= {x2}, x3 = {x3}\n")

class Subscriber:
    def __init__(self, p):
        self.p = p
        self.get_param(self.p)

    def encode(self, message):
        return pow_mod(message, self.c, self.p)

    def decode(self, message):
        return pow_mod(message, self.d, self.p)

    def get_param(self, p):
        self.c = get_rand()               
        nod, x, y = steroid_evklid(self.c, p - 1)

        while nod != 1 or x <= 0:
            self.c = get_rand()
            nod, x, y = steroid_evklid(self.c, p - 1)
        self.d = x * self.c



if __name__ == "__main__":
    cipers_shamir = Shamir()
    # cipers_shamir.shamir("pic.jpg", "out_pic.jpg")
    cipers_shamir.shamir("1.txt", "2.txt")