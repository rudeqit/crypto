#!/usr/bin/env python3

import random
import math

def sipmle_pow_mod(base: int, index_n: int, modulus: int) -> int:
    c: int = 1
    for index in range(index_n):
        c = (c * base) % modulus
    return c

### base ^ index_n % modulus 
def pow_mod(base: int, index_n: int, modulus: int) -> int:
    if index_n < 0:
        print(f"Error from pow_mod(): Can't do \"pow_mod\" with with negative index_n :(\
            \n({base} ^ {index_n} % {modulus})")
        return 0

    res: int = 1

    while index_n:
        if index_n & 0x1:
            res = (res * base) % modulus
        base = (base * base) % modulus
        index_n >>= 1

    return res

def gcd(a: int, b: int) -> int:
    if a == b: 
        return a
    if a < b: 
        (a, b) = (b, a)
    
    while b:
        tmp = b
        b = a % b
        a = tmp

    return a

### ax + by = gcd(a,b)
  # Input: a, b
  # gcd(a, b), x, y (as tuple)
def steroid_evklid(a: int, b: int) -> tuple:
    if a < b:
        print(f"Error from steroid_evklid(): Incorrect input value: {a:d} < {b:d}")
        return (0, 0, 0)

    U = (a, 1, 0)
    V = (b, 0, 1)
    
    # (u1, u2, u3) = U
    (v1, v2, v3) = V
    
    while V[0]:
        (u1, u2, u3) = U
        (v1, v2, v3) = V
        
        q = u1 // v1
        T = (u1 % v1, u2 - q*v2, u3 - q*v3)
        U = V
        V = T
    
    return U

# Y - open key
# X - Secret keys
def diffie_hellman(X_A: int, X_B: int, g: int, p: int) -> tuple:
    if g < 1 and g > (p - 1):
        print("Error from diffie_hellman(): Incorrect g and p variables")
        return (0, 0)

    # if not is_simple(p):
    #     print("Incorrect g variables: p is not prime")
    #     return (0, 0)

    Y_A = pow_mod(g, X_A, p)
    Y_B = pow_mod(g, X_B, p)

    Z_A = pow_mod(Y_B, X_A, p)
    Z_B = pow_mod(Y_A, X_B, p)

    return (Y_A, Y_B, Z_A, Z_B)

### Diffie Hallman with random generate value
def diff_hell(length: int = 10) -> tuple:
    X_A = get_rand(length)
    X_B = get_rand(length)

    while X_B == X_A:
        X_B = get_rand(length)

    g, p = get_g_p(length)

    Y_A, Y_B, Z_A, Z_B = diffie_hellman(X_A, X_B, g, p)

    print(f"g = {g:d}, p = {p:d}")
    print(f"X_A = {X_A:d}, Y_A = {Y_A:d}")
    print(f"X_B = {X_B:d}, Y_B = {Y_B:d}")

    if Z_A == Z_B:
        print(f"Z_A {Z_A:d} == {Z_B:d} Z_B")
    else:
        print(f"Z_A {Z_A:d} != {Z_B:d} Z_B\nI'm stupid asshole ;(")

    return ((p, g), (X_A, Y_A), (X_B, Y_B))

### Check n is simple or not
def is_simple(n) -> bool:
   d = 2
   while d * d <= n and n % d != 0:
       d += 1
   return d * d > n

### Generate g and p value for Diffie Hallman
def get_g_p(length: int = 10) -> tuple:
    q = get_rand_simple(length - 1)
    p = 2 * q + 1
    
    while not is_simple(p):
        q = get_rand_simple(length - 1)
        p = 2 * q + 1
    
    g = get_rand(length)
    while pow_mod(g, q, p) == 1 or g < 1 or g > (p - 1):
        g = get_rand(length - 3)

    return (g, p)

### Random number with given length
def get_rand(length: int = 10) -> int:
    rand_float: float = random.random()
    if rand_float <= 0.0:
        rand_float: float = random.random()

    l = length
    num_z = 1
    while l != 1:
        num_z *= 10
        l -= 1

    rand_float *= 10.0
    while round(rand_float) // num_z <= 0:
        rand_float *= 10.0

    return round(rand_float)

def get_rand_simple(length = 10) -> int:
    rand = 4

    while not is_simple(rand):
        rand = get_rand(length) 

    return rand

### y = (a ** x) mod p
  # return x
def step_baby_giant(y: int, a: int, p: int, m: int, k: int) -> int:
    if m * k < p:
        print(f"Error form step_baby_giant: Incorrect m and k values. m * k should be less then p")

    # (a ** (m - 1)) * y
    vector_j = []
    # (a ** (k * m)) 
    vector_i = []

    for j in range(0, m - 1):
        vector_j.append(pow_mod_bs(y, a, j, p))

    # print(vector_j)

    for i in range(0, k * m):
        vector_i.append(pow_mod(a, i * m, p))

        for j in range(0, len(vector_j)):
            if vector_j[j] == vector_i[i]:
                # print(vector_i)
                print(f"Find! j = {j:d}, i = {i:d}")
                x: int = i * m - j
                if x < 0:
                    print(f"But x = {x: d} < 0, mb we can find something else...")
                    break
                return x

    # print(vector_i)
    print("Can't find a^im = a^j*y")    
    return 0

def get_mut_prime(p: int) -> tuple:
    c = get_rand() % p               
    nod, x, y = steroid_evklid(p, c)

    while nod != 1 or y <= 0:
        c = get_rand() % p  
        nod, x, y = steroid_evklid(p, c)
    d = y

    # temp = (c * d) % (p)
    # print(f"c * d % p - 1 = {c} * {d} % {p} = {temp}")

    return c, d

### pow_mod for baby step baby giant (result * y)
def pow_mod_bs(y, a, m, p) -> int:
    if m == 0: 
        return y % p    
    t = pow_mod(a, m, p)
    return (t * y) % p

### m value for baby step baby giant
def get_m(p: int) -> int:
    return math.floor(math.sqrt(p)) + 1


### baby step baby giant with calculable m and k
def step_bg(y: int, a: int, p: int) -> int:
    m = get_m(p)
    k = m

    print(f"m = {m:d}, k = {k:d}")

    return step_baby_giant(y, a, p, m, k)


### Testing correct work baby step baby giant on random numbers
def step_bg_show(length: int = 10):
    a = get_rand(length)
    x = get_rand(length)
    p = get_rand(length)
    y = pow_mod(a, x, p)
    print(f"a = {a:d}, x = {x:d}, p = {p:d}, y = {y: d}")

    print(f"Try to find x: a ^ x % p = y")
    x_searching = step_bg(y, a, p)
    print(f"x = {x_searching:d}")

    print("Let's check x is true:")
    # print(f"a ^ x % p = y")
    y_checked = pow_mod(a, x_searching, p)
    print(f"{a:d} ^ {x_searching:d} % {p:d} = {y_checked:d}")
    if y == y_checked:
        print(f"{y:d} == {y_checked:d}")
    else:
        print(f"{y:d} != {y_checked:d}\nI'm stupid asshole ;(")

def main(length: int = 10):
    print("Pow mod operation(base ^ index_n % modulus)")
    # base = 43536065
    # index_n = 258012567
    # modulus = 407039523
    base = get_rand(length)
    index_n = get_rand(length)
    modulus = get_rand(length)
    pow_mod_res = pow_mod(base, index_n, modulus)
    print(f"\t{base:d} ^{index_n: d} % {modulus:d} = {pow_mod_res:d}")
    print("\n")

    print("Extended Euclidean algorithm (ax + by = gcd(a,b))")
    a = get_rand(length)
    b = get_rand(length)
    while a < b: a = get_rand(length)
    print(f"\t{a:d} * x + {b:d} * y = {gcd(a,b):d}")
    gcd_steroid, x, y = steroid_evklid(a, b)
    print(f"\tx = {x:d}, y = {y:d}, gcd({a:d}, {b:d}) = {gcd_steroid:d}")
    print("\n")

    print("Diffie Hallman algorithm")
    # (p, g), (X_A, Y_A), (X_B, Y_B) = diff_hell(length)
    diff_hell(length)
    print("\n")

    print("Baby step baby giant")
    step_bg_show(length)

if __name__ == "__main__":
    main(8)
