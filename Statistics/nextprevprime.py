from sympy import nextprime, prevprime
from time import perf_counter

def calc_prime(initial_code, n):
    start_time = perf_counter()

    left_prime = right_prime = initial_code

    for _ in range(n):
        left_prime = prevprime(left_prime)
        right_prime = nextprime(right_prime)

    result = left_prime*right_prime

    finish_time = perf_counter()

    return finish_time-start_time



for _ in range(50):
    random_file = open("../Client/random.txt", 'r')
    count = 0

    for num in random_file.readlines():
        initial_code, n = (int(value) for value in num.split())
        file = open("timesNextprevprime.txt", 'a')
        file.write(f'{calc_prime(initial_code, n)}\n')
        file.close()
        count += 1

        if count == 10:
            print(initial_code)
            break
