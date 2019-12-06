#!/usr/bin/env python3

### Add path to operations lib 
import random
import sys
sys.path.append("..")

from hashlib import sha256
from ciphers.el_gamal import ElGamal, Subscriber
from operations.operations import pow_mod, get_g_p, get_mut_prime

class ElGamalSign:
    
    def __init__(self):
        self.g, self.p = get_g_p()        
        self.alice = Subscriber(self.p, self.g) 

    def el_gamal_sign(self, file_in, file_sign=None):
        self.x = self.alice.c
        self.y = self.alice.d
        file_sign = str(file_in) + "_ElGamal_sign" if file_sign is None else file_sign

        with open(file_in, "rb") as fd_in:
            file = fd_in.read()
            h = sha256(file).digest()            
            # print(f"SHA256 hash: {self.y}")
            
        return self.get_rs(h, file_sign)
    
    def el_gamal_sign_check(self, file_in, file_sign=None):
        file_sign = str(file_in) + "_ElGamal_sign" if file_sign is None else file_sign
        
        rs = self.get_check_rs(file_sign)
        
        with open(file_in, "rb") as fd_in:
            file = fd_in.read()
            h = sha256(file).digest()

        valid, result_hash = self.compare_rs_hash(h, rs) 
        return valid

    def get_rs(self, h, file_sign):
        rr = []
        ss = []

        with open(file_sign, "w") as fd_sign:        
            for elem in h:
                k, k_inv = get_mut_prime(self.p - 1)
                r = pow_mod(self.g, k, self.p)
                u = (elem - (self.x * r)) % (self.p - 1)
                s = (k_inv * u) % (self.p - 1)

                rr.append(str(r) + "\n")
                ss.append(str(s) + "\n")
                fd_sign.write(str(r) + " " + str(s) + "\n")

                # self.print_debug_each_iter(elem, r, s, u, k, k_inv)

        return rr, ss

    def get_check_rs(self, file_sign, y=None, p=None):
        y = self.y if y is None else y
        p = self.p if p is None else p 

        result = []
        with open(file_sign, "r") as fd_sign:
            while True:
                rs = fd_sign.readline()
                if not rs:
                    break

                split = rs.split(" ")
                r = int(split[0])
                split2 = split[1].split("\n")
                s = int(split2[0])
                
                # print(r, s)

                res = (pow_mod(y, r, p) * pow_mod(r, s, p)) % p
                # print(f"res {res}")
                result.append(res)

        return result 

    def compare_rs_hash(self, h, rs, p=None, g=None):
        valid = True

        p = self.p if p is None else p
        g = self.g if g is None else g
        result = []

        for elem_h, elem_rs in zip(h, rs):
            res = pow_mod(g, elem_h, p)
            print(f"{res} = {elem_rs}")
            
            valid = res == elem_rs
            if not valid:
                print("Error! ElGamal signature is bullshit")
                return valid

            result.append(res)    

        if valid:
            print("Great! ElGamal signature is authentic")

        return valid, result

    def print_debug_each_iter(self, elem, r, s, u, k, k_inv):
        print(f"h_elem = {elem}")
        print(f"u = {elem} - {self.x} * {r} % {self.p} - 1 = {u}")
        print(f"Check k: k * k^-1 % p - 1 = {k} * {k_inv} % {self.p - 1} = {(k * k_inv) % (self.p - 1)}")                
        print(f"r = {r}, s = {s}")
        
        print("Check result:")
        res1 = (pow_mod(self.y, r, self.p) * pow_mod(r, s, self.p)) % self.p
        res2 = pow_mod(self.g, elem, self.p)
        print(f"{res1} = {res2}\n")

if __name__ == "__main__":
    # file_in = "1.txt"
    file_in = "pic.jpg"

    el_gamal_sign = ElGamalSign()
    el_gamal_sign.el_gamal_sign(file_in)
    el_gamal_sign.el_gamal_sign_check(file_in)