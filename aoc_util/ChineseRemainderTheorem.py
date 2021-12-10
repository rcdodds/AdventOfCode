import numpy as np
import math
from collections import Counter


class NonIntegerRemainderError(Exception):
    """Input array of remainders includes non-integer(s)"""
    pass


class NonCoprimeDivisorsError(Exception):
    """Input array of divisors includes elements that are not coprime"""
    pass


class DuplicateDivisorsError(Exception):
    """Input array of divisors includes duplicate elements"""
    pass


def check_integers(numbers):
    # If any of the inputs have remainders other than 0 when divided by 1, they are not integers
    if not np.product((np.equal(np.mod(numbers, 1), 0))):
        raise NonIntegerRemainderError
    # Validation has passed
    else:
        return True


def check_coprime(divisors):
    # If a divisor is present twice, it is not coprime by definition
    if len([d for d, count in Counter(divisors).items() if count > 1]):
        raise DuplicateDivisorsError
    # If any combinations of non-duplicate divisors has a GCD > 1, they are not coprime
    elif max([math.gcd(i, j) for i in divisors for j in divisors if i != j]) > 1:
        raise NonCoprimeDivisorsError
    # Both validations have passed
    else:
        return True


def solve_crt(modulus_array, remainder_array):
    """
    System of Equations
        x % n_1 = b_1
        x % n_2 = b_2
        ...
        x % n_k = b_k

    Pre-requisites
        (1) n_i's must be coprime
        (2) b_i's can be any integers

    Inputs
        :param modulus_array:       Numpy array of modulus divisors (n_i's)
        :param remainder_array:     Numpy array of remainders (b_i's)

    Processing
        (1) Calculate  N = n_1 * n_2 * ... n_k
        (2) For each b_i, calculate N_i = N / n_i
        (3) Find the inverse of each N_i (called x_i) - i.e. (N_i * x_i) % n_i = 1

    Output
        (1) Minimum positive solution
        (2) Modulo that solution is unique with respect to
    """
    # Check for pre-requisites
    if check_coprime(modulus_array) and check_integers(remainder_array):
        # Get ready for large numbers
        modulus_array = modulus_array.astype(np.int64)
        remainder_array = remainder_array.astype(np.int64)

        # Processing Step 1 - Multiply all modulus divisors together
        mod_product = np.product(modulus_array)

        # Processing Step 2 - Divide each modulus divisor into the overall modulus product
        N_i_array = np.int64(mod_product / modulus_array)

        # Processing Step 3 - Determine the inverse of each n_i
        x_i_array = np.array([pow(int(N_i_array[i]), -1, int(modulus_array[i])) for i in range(len(N_i_array))])

        # Processing Step 4 - Return minimum solution and repeat increment
        product_bNx = remainder_array * N_i_array * x_i_array
        sum_bNx = np.sum(product_bNx)
        min_pos_solution = sum_bNx % mod_product

        # Confirm solution is correct per original requirements
        actual_remainders = int(min_pos_solution) % modulus_array
        print('CRT Confirmation\nRequired Remainders\n', remainder_array, '\nActual Remainders\n',  actual_remainders, '\n')

        return min_pos_solution, mod_product
