import random


# Miller-Rabin test to check if given number is prime
def is_prime_miller_rabin(n, k=8):
    if n == 2 or n == 3:
        return True

    if n % 2 == 0:
        return False

    s, d = 0, n - 1
    while d % 2 == 0:
        s += 1
        d //= 2
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False

    return True


def get_random(bit_length):
    start = pow(2, bit_length - 1)
    end = pow(2, bit_length) - 1
    return random.randint(start, end)


def gen_prime(bit_length):
    while True:
        random_number = get_random(bit_length)
        if is_prime_miller_rabin(random_number):
            return random_number
