#!/usr/bin/env python3

### Add path to operations lib 
import random
import sys
sys.path.append("../operations")

from operations import diff_hell, pow_mod, pow_mod_bs, get_rand_simple, get_rand, get_g_p

class ElGamal:
    def __init__(self):
        self.g, self.p = get_g_p()
        self.alice = Subscriber(self.p, self.g)
        self.bob = Subscriber(self.p, self.g)

    def el_gamal(self, file_in, file_out):
        with open(file_in, "rb") as fd_in, open(file_out, "wb") as fd_out:
            while True:
                ### Read file byte to byte
                num_bytes = 1 
                element = fd_in.read(num_bytes)
                if not element:
                    break

                el = int.from_bytes(element, byteorder="little")

                r, e = self.alice.encode(el, self.bob.d)
                decode_el = self.bob.decode(r, e)

                ### Write decode info in file
                self.log(r, e)
                fd_out.write(decode_el.to_bytes(num_bytes, byteorder="little"))

    def log(self, r, e, keys_file = "ElGamel_Keys.txt", decode_value = "ElGamel_Decode.txt"):
        with open(keys_file, "a") as fd_kf, open(decode_value, "a") as fd_df:
            fd_kf.write(f"p = {self.p}, g = {self.p}, \
                \n{self.alice.c}, da = {self.alice.d}, \
                \ncb = {self.bob.c}, db = {self.bob.d}\n")
            fd_df.write(f"r = {r}, e = {e}\n")


class Subscriber:
    def __init__(self, p, g):
        self.p = p
        self.g = g
        self.c = random.randint(1, self.p - 1)
        self.d = pow_mod(self.g, self.c, self.p)

    def encode(self, message, d) -> tuple:
        k = random.randint(1, self.p - 2)
        r = pow_mod(self.g, k, self.p)
        e = pow_mod_bs(message, d, k, self.p)
        return r, e

    def decode(self, r, e):
        return pow_mod_bs(e, r, self.p - 1 - self.c, self.p)
        

if __name__ == "__main__":
    cipers_el_gamal = ElGamal()
    cipers_el_gamal.el_gamal("pic.jpg", "out_pic.jpg")
    # cipers_el_gamal.el_gamal("1.txt", "2.txt")
