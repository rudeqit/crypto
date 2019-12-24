#!/usr/bin/env python3

### Add path to operations lib 
import sys
sys.path.append("..")

from operations.operations import pow_mod, get_rand_simple, get_rand, steroid_evklid, gcd, is_simple

LOG = True

class RSA:

    def __init__(self):
        self.alice = Subscriber()
        self.bob = Subscriber()
        self.print_info()

    def rsa(self, file_in, file_out):
        ### Log shit
        enc = []

        with open(file_in, "rb") as fd_in, open(file_out, "wb") as fd_out:
            while True:
                ### Read file byte to byte
                num_bytes = 1 
                element = fd_in.read(num_bytes)
                if not element:
                    break

                el = int.from_bytes(element, byteorder="little")

                alice_encode = self.alice.encode(el, self.bob.d, self.bob.N)
                bob_decode = self.bob.decode(alice_encode)

                ### Should be equal
                # print(el)
                # print(bob_decode)

                if LOG:
                    enc.append(f"{alice_encode}\n")
                ### Write decode info in file

                fd_out.write(bob_decode.to_bytes(num_bytes, byteorder="little"))
        
        if LOG:
            self.write_keys()
            self.log(enc)

        print(f"Hello from RSA cipher!")
        print(f"Alice encode file \'{file_in}\' and send it to Bob.")
        print(f"Bob recv msg, decode and save it in \'{file_out}\'.")

    def write_keys(self, rsa_pub = "rsa.pub", rsa_private = "rsa"):
        with open(rsa_pub, "w") as fd_rpb, open(rsa_private, "w") as fd_rpv:
            fd_rpb.write(f"Alice:\n\td = {self.alice.d}, N = {self.alice.N}\
                \nBob:\n\td = {self.bob.d}, N = {self.bob.N}\n")
            
            fd_rpv.write(f"Alice secret:\n\tc = {self.alice.c}\
                \nBob secret:\n\tc = {self.bob.c}\n")

    def log(self, encode, rsa_encode = "rsa_encode"):
        with open(rsa_encode, "w") as fd_en:
            
            for elem in encode:
                fd_en.write(elem)

    def print_info(self):
        print(f"Alice:\n\tP = {self.alice.P}, Q = {self.alice.Q} N = {self.alice.N}\
            \n\tFi = {self.alice.fi}, c = {self.alice.c}, d = {self.alice.d}")
        print(f"(alice.c * alice.d % alice.fi)) = {(self.alice.c * self.alice.d % self.alice.fi)}")
        print(f"gcd(alice.d, alice.fi) = {gcd(self.alice.d, self.alice.fi)}")
         
        print(f"Bob:\n\tP = {self.bob.P}, Q = {self.bob.Q} N = {self.bob.N}\
            \n\tFi = {self.bob.fi}, c = {self.bob.c}, d = {self.bob.d}")
        print(f"(bob.c * bob.d % bob.fi)) = {(self.bob.c * self.bob.d % self.bob.fi)}")
        print(f"gcd(bob.d, bob.fi) = {gcd(self.bob.d, self.bob.fi)}")


class Subscriber:

    def __init__(self, P=None, Q=None, c=None, d=None):
        self.P = get_rand_simple(5) if P is None else P
        self.Q = get_rand_simple(5) if Q is None else Q
        if self.P == self.Q:
            raise ValueError(f"self.P == self.Q ({self.P} == {self.Q})")

        self.N = self.P * self.Q

        # Here should be check P and Q is prime 

        self.get_param(c, d)
        
    def get_param(self, c=None, d=None):
        self.fi = (self.P - 1) * (self.Q - 1)

        if c is None and d is None:
            self.c = c
            self.d = d
            pass
        
        self.c = get_rand() % (self.fi - 1)
        
        nod, x, y = steroid_evklid(self.fi, self.c)
        while nod != 1 or y <= 0:
            self.c = get_rand() % (self.fi)
            nod, x, y = steroid_evklid(self.fi, self.c)
        self.d = y 

    def encode(self, message, d, N):
        return pow_mod(message, d, N)

    def decode(self, e):
        return pow_mod(e, self.c, self.N)

if __name__ == "__main__":
    # file_in, file_out = "pic.jpg", "out_pic.jpg"
    file_in, file_out = "1.txt", "2.txt"     

    cipers_rsa = RSA()
    cipers_rsa.rsa(file_in, file_out)
