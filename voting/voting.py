#!/usr/bin/env python3

# Add path to our lib
import hashlib
import random
import sys
sys.path.append("..")

from operations.operations import pow_mod, get_mut_prime
from ciphers.RSA import Subscriber
from prime import gen_prime

class Server:

    def __init__(self):
        self.dudes = []
        self.voices = []

        self.P, self.Q = gen_prime(1024), gen_prime(1024)
        self.sub = Subscriber(self.P, self.Q)
        self.N = self.sub.N
        self.c = self.sub.c
        self.d = self.sub.d

        # print(f"d = {self.d}\nN = {self.N}")
    
    def get_dn(self):
        return self.d, self.N

    def check_dude(self, h, rnd):
        if rnd in self.dudes:
            raise ValueError(f"WAIT, THATS ILLEGAL."
                             f"Dude with rnd {rnd} came twice")
        
        self.dudes.append(rnd)        
        return self.sub.decode(h)
        # return pow_mod(h, self.c, self.N)


    def check(self, n, s):
        _n = self.sub.encode(s, self.d, self.N) 
        # _n = pow_mod(s, self.d, self.N)
        if n != _n:
            print(f"Ops, {n} != {_n}")
            pass

        print(f"Alright dude, u good\n\t({n} == {_n})")
        self.voices.append(n)

class Dude:

    def __init__(self, N):
        self.N = N
        self.rnd = random.getrandbits(512)

    def get_n(self, voice: int):
        self.n = (self.rnd << 1) | voice
        return self.n

    def get_r(self):
        self.r, self._r = get_mut_prime(self.N)
        return self.r, self._r

    def gen_sha256(self, data):
        generator = hashlib.sha256()

        if type(data) is str:
            generator.update(data.encode())
        elif type(data) is bytes:
            generator.update(data)

        return generator.hexdigest()
    
    def get_hash(self, d):
        self.h = int(self.gen_sha256(str(self.n)), 16)
        self.h_serv = (self.h * pow_mod(self.r, d, self.N)) % self.N
        return self.h_serv

    def get_blank(self, _s):
        self.s = (self._r * _s) % self.N
        return self.h, self.s

class Voting:

    def __init__(self):
        self.server = Server()

    def vote(self):
        d, N = self.server.get_dn()
        dude = Dude(N)

        print(f"Dude, do u want to sleep? (y or n)")
        voice = input()
        if voice == "y" or voice == "yes":
            print("I also want to, bro")
            v = 1
        elif voice == "q":
            print("Voiting is over.")
            return False
        else:
            print("U do not want?! OK.")
            v = 0
    
        n = dude.get_n(v)
        r, _r = dude.get_r()

        _s = self.server.check_dude(dude.get_hash(d), dude.rnd)
        
        n, s = dude.get_blank(_s)

        self.server.check(n, s)
        
        print()
        
        return True         


if __name__ == "__main__":
    voting = Voting()

    status = True
    while status:
        status = voting.vote()