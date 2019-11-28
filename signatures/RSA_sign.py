#!/usr/bin/env python3

### Add path to operations lib 
import sys
from hashlib import sha256
sys.path.append("..")

from ciphers.RSA import RSA, Subscriber
from operations.operations import pow_mod

class RSA_sign:
    def __init__(self):
        self.alice = Subscriber()

    def rsa_sign(self, file_in, file_sign=None):
        file_sign = str(file_in) + "_RSA_sign" if file_sign is None else file_sign

        with open(file_in, "rb") as fd_in, open(file_sign, "w") as fd_sigh:
            file = fd_in.read()
            self.y = sha256(file).digest()            
            # print(f"SHA256 hash: {self.y}")
            
            s = self.get_s()
            for elem in s:
                # print(elem)
                fd_sigh.write(str(elem) + "\n")

            return s

    def rsa_sign_check(self, file_in, file_sign=None):
        file_sign = str(file_in) + "_RSA_sign" if file_sign is None else file_sign
        with open(file_in, "rb") as fd_in:
            w = self.get_w(file_sign)
            
            file = fd_in.read()
            y = sha256(file).digest()

            print(f"{self.y}")
            print(bytes(self.w))

    def get_s(self, y=None, c=None, N=None):
        y = self.y if y is None else y
        c = self.alice.c if c is None else c
        N = self.alice.N if N is None else N
        
        self.s = []
        for elem in self.y:
            # print(elem)
            self.s.append(pow(elem, c, N))
        
        return self.s

    def get_w(self, file_sign, d=None, N=None):
        d = self.alice.d if d is None else d
        N = self.alice.N if N is None else N
        self.w = []

        with open(file_sign, "r") as fd_sign:
            while True:
                s_num = fd_sign.readline()
                if not s_num:
                    break
                self.w.append(pow_mod(int(s_num), d, N))
        
        return self.w

if __name__ == "__main__":
    # file_in = "1.txt"
    file_in = "pic.jpg"

    rsa_sign = RSA_sign()
    rsa_sign.rsa_sign(file_in)
    rsa_sign.rsa_sign_check(file_in)
    
