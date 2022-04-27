from sympy import isprime
from time import perf_counter

def calc_prime(initial_code, n):
    start_time = perf_counter()

    upper_prime = lower_prime = initial_code
    upper_primes_counter = lower_primes_counter = 0

    while upper_primes_counter < n or lower_primes_counter < n:
        if upper_primes_counter < n:
            upper_prime += 1

            if isprime(upper_prime):
                upper_primes_counter += 1

        if lower_primes_counter < n:
            lower_prime -= 1

            if isprime(lower_prime):
                lower_primes_counter += 1

    result = lower_prime*upper_prime

    finish_time = perf_counter()

    return finish_time-start_time


for _ in range(50):
    random_file = open("../Client/random.txt", 'r')
    count = 0

    for num in random_file.readlines():
        initial_code, n = (int(value) for value in num.split())
        file = open("timesIsprime.txt", 'a')
        file.write(f'{calc_prime(initial_code, n)}\n')
        file.close()
        count += 1

        if count == 10:
            print(initial_code)
            break
