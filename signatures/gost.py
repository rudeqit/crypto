#!/usr/bin/env python3

### Add path to operations lib 
import random
import sys
sys.path.append("..")

from hashlib import sha256
from ciphers.el_gamal import ElGamal, Subscriber
from operations.operations import pow_mod, get_g_p, get_mut_prime, is_simple, steroid_evklid

class GostSign:
    def __init__(self):
        ### Gen p,q,b
        q = random.randint(2 ** 16, 2 ** 17 - 1)
        p = random.randint(2 ** 31, 2 ** 32 - 1)
        b = int((p - 1) / q)
        p = b * q + 1

        while not (is_simple(p) and is_simple(q)):
            q = random.randint(2 ** 16, 2 ** 17 - 1)
            p = random.randint(2 ** 31, 2 ** 32 - 1)
            b = int((p - 1) / q)
            p = b * q + 1

        ## Gen a 
        a = random.randint(1, p - 1)
        temp = pow_mod(a, b, p)
        while temp != 1:
            a = random.randint(1, p - 1)
            temp = pow_mod(a, q, p)

        self.p = p
        self.q = q
        self.b = b
        self.a = a

        self.x = random.randint(1, self.q - 1)
        self.y = pow_mod(self.a, self.x, self.p)


    def gost_sign(self, file_in, file_sign=None):
        file_sign = str(file_in) + "_gost_sign" if file_sign is None else file_sign

        with open(file_in, "rb") as fd_in:
            file = fd_in.read()
            h = sha256(file).digest()

        return self.get_rs(h, file_sign) 
    
    def gost_sign_check(self, file_in, file_sign=None):
        file_sign = str(file_in) + "_gost_sign" if file_sign is None else file_sign
        
        r, s = self.read_rs(file_sign)
        
        with open(file_in, "rb") as fd_in:
            file = fd_in.read()
            h = sha256(file).digest()

        valid, result_r = self.compare_rs_hash(h, r, s) 
        return valid

    def get_rs(self, h, file_sign, q=None, p=None, a=None, x=None):
        q = self.q if q is None else q
        p = self.p if p is None else p 
        a = self.a if a is None else a
        x = self.x if x is None else x
        y = self.y

        rr = []
        ss = []

        with open(file_sign, "w") as fd_sign:        
            for elem in h:
                if elem > q:
                    print("Error in gost signature! Some byte in hash more than q")
                    return None, None

                k = random.randint(0, q)
                r = pow_mod(a, k, p) % q
                s = (k * elem + x * r) % q
                
                while r == 0 or s == 0:
                    k = random.randint(0, q)
                    r = pow_mod(a, k, p) % q
                    s = (k * elem + x * r) % q

                # self.print_debug_each_iter(elem, p, q, r, s, k, x, y, a)

                rr.append(str(r) + "\n")
                ss.append(str(s) + "\n  ")
                fd_sign.write(str(r) + " " + str(s) + "\n")

        return rr, ss

    def read_rs(self, file_sign, y=None, p=None):
        y = self.y if y is None else y
        p = self.p if p is None else p 

        rr = []
        ss = []

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

                rr.append(r)
                ss.append(s)

        return rr, ss 

    def compare_rs_hash(self, h, rr, ss, p=None, q=None, a=None, y=None):
        valid = True
        p = self.p if p is None else p
        q = self.q if q is None else q
        a = self.a if a is None else a
        y = self.y if y is None else y
        result_r = []

        print("Check result:")
        for elem, r, s in zip(h, rr, ss):
            if r < 0 or r > q:
                valid = False
                print(f"Error in gost sign! uncorrect r: 0 < {r} < {q}")
                return valid, None
            
            if s < 0 or s > q:
                valid = False
                print(f"Error in gost sign! uncorrect s: 0 < {s} < {q}")
                return valid, None

            nod, x1, y1 = steroid_evklid(q, elem)
            h1 = y1  # (x % f + f) % f
            if h1 < 0:
                h1 = h1 + q
            # print(f"Check h: h * h^-1 % p = {elem} * {h1} % {q} = {(elem * h1) % (q)}")

            u1 = (s * h1) % q
            u2 = ((-1 * r) * h1) % q
            r2 = ((pow_mod(a, u1, p) * pow_mod(y, u2, p)) % p) % q 
            
            print(f"{r} = {r2}")
            valid = r == r2
            if not valid:
                print("Error! Gost signature is bullshit")
                return valid, None

            result_r.append(r2)    

        if valid:
            print("\nGreat! Gost signature is authentic")

        return valid, result_r

    def print_debug_each_iter(self, elem, p, q, r, s, k, x, y, a):
        print(f"h_elem = {elem}")
        print(f"r: 0 < {r} < {q}, s: 0 < {s} < {q}")

        nod, x1, y1 = steroid_evklid(q, elem)
        h1 = y1  # (x % f + f) % f
        if h1 < 0:
            h1 = h1 + q
        print(f"Check h: h * h^-1 % p = {elem} * {h1} % {q} = {(elem * h1) % (q)}")
        
        print("Check result:")
        u1 = (s * h1) % q
        u2 = ((-1 * r) * h1) % q
        r2 = ((pow_mod(a, u1, p) * pow_mod(y, u2, p)) % p) % q 
        print(f"{r} = {r2}\n")

if __name__ == "__main__":
    # file_in = "1.txt"
    file_in = "pic.jpg"

    gost_sign = GostSign()
    gost_sign.gost_sign(file_in)
    gost_sign.gost_sign_check(file_in)