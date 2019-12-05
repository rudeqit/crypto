#!/usr/bin/env python3

### Add path to operations lib 
import random
import sys
sys.path.append("..")

from operations.operations import pow_mod, pow_mod_bs, get_g_p

LOG = True

class ElGamal:

    def __init__(self):
        self.g, self.p = get_g_p()
        self.alice = Subscriber(self.p, self.g)
        self.bob = Subscriber(self.p, self.g)

    def el_gamal(self, file_in, file_out):
        ### Log shit
        re = []

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

                ### Should be equal
                # print(el)
                # print(decode_el)

                if LOG:
                    re.append(f"{r}\t{e}\n")

                ### Write decode info in file
                fd_out.write(decode_el.to_bytes(num_bytes, byteorder="little"))
        if LOG:
            self.log(re)
        
        print(f"Hello from ElGamal cipher!")
        print(f"Alice encode file \'{file_in}\' and send it to Bob.")
        print(f"Bob recv msg, decode and save it in \'{file_out}\'.")
    
    def log(self, re, keys_file = "el_gamal_keys", encode_file = "el_gamal_encode"):
        with open(keys_file, "w") as fd_kf, open(encode_file, "w") as fd_ef:
            
            fd_kf.write(f"p = {self.p}\tg = {self.p} \
                \nca = {self.alice.c}\tda = {self.alice.d} \
                \ncb = {self.bob.c}\tdb = {self.bob.d}\n")
            
            for enc_str in re:
                fd_ef.write(enc_str)


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
    # file_in, file_out = "pic.jpg", "out_pic.jpg"
    file_in, file_out = "1.txt", "2.txt"     
    
    cipers_el_gamal = ElGamal()
    cipers_el_gamal.el_gamal(file_in, file_out)
