#!/usr/bin/env python3

### Add path to operations lib 
import sys
sys.path.append("..")

from random import shuffle

from operations.operations import pow_mod, get_mut_prime, get_rand
from ciphers.RSA import Subscriber as SubRsa
from graph import Graph

# An attempt to fool the Bob if True
CHEATING = False

class Hamilton:

    def __init__(self, G=None, hamltn_path=None):  
        self.init_G_and_path(G, hamltn_path)    
        self.init_subs()
        
        
    def init_subs(self):
        self.alice = Subscriber(self.G, self.hamltn_path)
        self.bob = Subscriber(self.G)

    def init_G_and_path(self, G=None, hamltn_path=None):
        self.graph = Graph(5, 70)
        hamltn_path = self.graph.hamilton()
        if G is None:
            while len(hamltn_path) == 0:
                self.graph = Graph(5, 70)
                hamltn_path = self.graph.hamilton()
            
            self.G = self.graph.matrix
            self.hamltn_path = hamltn_path[0]
        else:
            self.G = G
            self.hamltn_path = hamltn_path

        return self.G, self.hamltn_path

    # Do Alice stuff
    def start(self, G=None, hamltn_path=None):
        # TODO add input G matrix (from file) and hamltn_path

        print("G:")
        self.graph.print_neighbours_list()

        print()
        for line in self.G:
            print(line)

        print(f"\n===========================")
        print("Alice moves:\n")
        H, H_order = self.alice.encode_G(self.G)
        print(f"Get H order: {H_order}")
        print("Get H:")
        self.print_matrix(H)

        _H = self.alice.encode_H(H)
        print("Get _H:")
        self.print_matrix(_H)

        F = self.alice.encode__H(_H, self.bob.rsa.d, self.bob.rsa.N)
        print("F to Bob:")
        self.print_matrix(F)
        

        path_in__H = self.alice.encode_path(self.hamltn_path, self.G, H_order, _H)
        print("And got hamilton path in _H:")
        print(path_in__H)

        print("\n===========================")

    def choice(self, F=None, H_order=None, path_in__H=None):
        F = self.alice.F if F is None else F
        H_order = self.alice.H_order if H_order is None else H_order
        path_in__H = self.alice.path_in__H if path_in__H is None else path_in__H
        
        one = False
        two = False

        print(f"\nHello Bob!\nI'm Alice and i know a Hamilton path for G.\n"
              f"U have two options.\nWhat u choose the first?\n")

        while one is False or two is False:
            if one is False:
                print("1. What a Hamiltonian cycle for H?")
            if two is False:
                print("2. Confirm that H is isomorphic G")

            choice = input()
            if choice == "1" and one is False:
                self.encode_path(F, path_in__H)
                one = True

            elif choice == "2" and two is False:
                self.encode_matrix(F, H_order)
                two = True

    def encode_matrix(self, F, H_order):
        print(f"\n===========================")
        print(f"Bob encode matrix:\n")
        print("Recive F from Alice:")
        self.print_matrix(F)

        _H = self.bob.decode_F(F)
        print("Decode F, get _H:")
        self.print_matrix(_H)

        H = self.bob.decode__H(_H)
        print("Decode _H, get H:")
        self.print_matrix(H)

        G = self.bob.decode_H(H, H_order)
        print("Decode H, get G:")
        self.print_matrix(G)

        if self.G == G:
            print("Bob get right G, validation OK!")
        else:
            raise ValueError("Error! Alice cheating!\nWrong F matrix.")

        print("===========================")

    def encode_path(self, F, path_in__H):
        print(f"\n===========================")
        print(f"Bob check path:\n")
        
        print("Recive F from Alice:")
        self.print_matrix(F)
        
        print("Recive path from Alice:")
        print(path_in__H)

        _H = self.bob.decode_F(F)
        print("Decode F, get _H:")
        self.print_matrix(_H)

        print("Checking Vertices...")
        check_vertices = self.check_vertices(F, _H, path_in__H)
        if check_vertices != True:
            raise ValueError("Error! Alice cheating!\nNot valid _H matrix.")
        print(f"Check Vertices, all is correct!")

        print("\nChecking cycle...")
        visit_nodes = self.visit_nodes(self.G, path_in__H)
        if visit_nodes != True:
            raise ValueError("Error! Alice cheating!\nNot correct cycle.")
        print(f"Check Hamiltonian cycle for _H, all is correct!")

        print("===========================")

    def check_vertices(self, F, _H, path_in__H) -> bool:
        keys = list(path_in__H.keys())
        for elem in keys:
            i, j = path_in__H.get(elem)
            if elem != _H[i][j]:
                print(f"{elem} != {_H[i][j]}")    
                return False
            print(f"{elem} == {_H[i][j]}")

        return True

    def visit_nodes(self, G, path_in__H) -> bool:
        visit = {}

        for i in range(1, len(G)):
            v = {i: False}
            visit.update(v) 

        keys = list(path_in__H.keys())
        
        if len(keys) != (len(G) - 1):
            return False
        
        for elem in keys:
           i, j = path_in__H.get(elem)
           
           if visit.get(i) == True:
                return False
           
           v = {i: True}
           visit.update(v)

        print(f"{visit}")

        for i in range(1, len(G)):
            if visit.get(i) == False:
                return False
           
        return True 
                    
    def print_matrix(self, matrix):
        for line in matrix:
            print(line) 
        print()


class Subscriber:

    def __init__(self, G=None, hamltn_path=None):
        self.rsa = SubRsa()
        self.G = [] if G is None else G     # Исходная матрица
        self.H = []                         # Изоморф
        self.H_order = []                   # Нумерация вершин после перестановки
        self._H = []                        # r || H
        self.F = []                         # Зашифрованная матрица
        self.hamltn_path = [] if hamltn_path is None else hamltn_path

    # return H
    def encode_G(self, G):
        H = []
        H_order = [i for i in range (1, len(G))]
        shuffle(H_order)

        H.append(G[0])
        for index in H_order:
            H.append(G[index]) 
        
        self.G = G
        self.H = H
        self.H_order = H_order
        return H, H_order
    
    # return _H
    def encode_H(self, H):
        _H = []
        _H_line = []
        _H_line_rand = []


        for line in H:            
            for elem in line:
                rand = get_rand(8)

                elem = (~1 & rand) + elem
                _H_line.append(elem)

            _H.append(_H_line)
            _H_line = []

        self._H = _H
        return _H

    # return F
    def encode__H(self, _H, d, N):
        F = []
        F_line = []

        for line in _H:
            for elem in line:
                F_line.append(self.rsa.encode(elem, d, N))

            F.append(F_line)
            F_line = []

        self.F = F
        return F

    # return dict with hamilton path for _H graph
    def encode_path(self, path, G, H_order, _H):
        path_dict = {}
        for i, index in zip(range(0, len(path)), range(1, len(G))):
            vertices_dict = {path[i]: ([path[i], path[i + 1]])}
            path_dict.update(vertices_dict)

        # print(f"path_dict: {path_dict}")

        assoc_dict = {}
        for i, elem in zip(range(1, len(G) + 1), H_order):
            _dict = {i: elem}  
            assoc_dict.update(_dict)

        # print(f"assoc_dict: {assoc_dict}")
      
        _path_in__H = {}
        keys = list(path_dict.keys())
        for i in keys:
            i_dict = path_dict.pop(i)
            ass_i_key = assoc_dict.get(i)
            ass_i_val = []
            for elem in i_dict:
                ass_i_val.append(assoc_dict.get(elem))
            
            _dict = {ass_i_key: ass_i_val}
            _path_in__H.update(_dict)

        # print(f"_path_in__H: {_path_in__H}")

        path_in__H = {}
        keys = list(_path_in__H.keys())
        for elem in keys:
            value = _path_in__H.get(elem)
            i, j = value
            ass_i_key = _H[i][j]
            
            _in_H = {ass_i_key: value}
            path_in__H.update(_in_H)

        if len(list(_path_in__H.keys())) != len(list(path_in__H.keys())):
            raise ValueError("Oops, dictionary have a several identical keys.\nFix it u fucker")
        
        self.path_in__H = path_in__H
        return path_in__H

    # return F
    def decode_F(self, F):
        _H = []
        _H_line = []

        for line in F:
            for elem in line:
                _H_line.append(self.rsa.decode(elem))

            _H.append(_H_line)
            _H_line = []

        self.F = F
        self._H = _H

        return _H

    # return H
    def decode__H(self, _H):
        H = []
        H_line = []

        for line in _H:
            for elem_H in line:
                H_line.append(elem_H & 1)

            H.append(H_line)
            H_line = []

        self._H = _H
        self.H = H

        return H
    
    # return G
    def decode_H(self, H, H_order):
        G = H.copy()

        G[0] = H[0] 
        for index, i in zip(H_order, range(1, max(H_order) + 1)):
            G[index] = H[i]

        self.H = H
        self.H_order = H_order
        self.G = G

        return G

if __name__ == "__main__":
    hamilton = Hamilton()
    # G = [[0, 0, 0, 0, 0, 0], 
    #      [0, 0, 1, 0, 1, 1], 
    #      [0, 1, 0, 0, 1, 1], 
    #      [0, 0, 0, 0, 1, 1], 
    #      [0, 1, 1, 1, 0, 0], 
    #      [0, 1, 1, 1, 0, 0]
    #     ]
    # Hamilton cicle: 
    # cycle = [1, 2, 5, 3, 4, 1]

    if CHEATING == True:
        F = [[3222046218, 1281272768, 3276473528, 1194586434, 2465686281, 1007876526],
            [2504475748, 2816684159, 785543551, 2305825651, 1468023579, 2827338286],
            [2035756572, 1995369228, 2739916856, 3512887365, 1227616965, 3009832353],
            [747668398, 2119893495, 1584035266, 1619342890, 385660926, 2606875985],
            [2903238816, 1535490981, 2632479804, 662627484, 2463519915, 377174387],
            [1274675079, 419165783, 2780548527, 2901603500, 3136710429, 2047370671]]
        _H_order = [5, 3, 1, 4, 2]
        path_in__H = {12275037: [5, 3], 51561456: [3, 4], 97850181: [4, 2], 37313315: [2, 1], 51223456: [1, 5]}

        hamilton.choice(F, _H_order, path_in__H)

    hamilton.start()
    hamilton.choice()