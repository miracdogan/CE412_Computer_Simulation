import math

# a value = 16807
# m value = 2147483647

N = int(input("Number of random numbers: "))  # Getting input from users
x0 = int(input("x0 value: "))  # Getting input from users
a = int(input("a value with base 10: "))  # Getting input from users
c = int(input("c value with base 10: "))  # Getting input from users
m = int(input("m value with base 10: "))  # Getting input from users


def linear_congruential_method(N, x0, a, c, m):  # Create a function for create the numbers
    arr = []  # Create an array for store the generated numbers.
    xn = x0
    for i in range(N):
        xn = (a * xn + c) % m  # Apply the formula.
        arr.append(xn)  # Appending created numbers in to the array.

    print(" ")
    print("Numbers Divided by m")
    for i in range(arr[i]):  # Print numbers first three digit.
        print('%6.3f' % (arr[i] / m))
        i += 1
        if i == N:
            break

    print(" ")
    print("Numbers In Array, Not Divided by m")
    return arr  # Return Array


print(linear_congruential_method(N, x0, a, c, m))

ks_test = (1.36 / math.sqrt(N))     # Formula for K-S Test
print(" ")
print("KS Test Result: ", ks_test)
a = 0.05

if ks_test < ks_test * a:   # Compare the situation then print the result.
    print("Uniform")
else:
    print("Not Uniform")
