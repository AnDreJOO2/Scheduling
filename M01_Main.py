

from time import process_time






#Różny czas rzeczywisty przy wykonaniu programu wynika z faktu że procesor kolejkuje zadania w systemie i decyduje w którym momencie wykona nasz program

def power(a, n, m):
    ### POCZATEK ROZWIAZANIA
    o = 1
    for i in range(n):
        o = (a*o)%m
    return o
    ### KONIEC ROZWIAZANIA


from random import gauss

for length in [100, 200, 300, 1000, 10000]:
    f = open(f"Giełda_{length}.txt", "w")

    ### POCZATEK ROZWIAZANIA
for length in [100, 200, 300, 1000, 10000]:
    f = open(f"Giełda_{length}.txt", "w")
    for x in range(length):
        number = gauss(2, 25)
        f.write(str(number) + "\n")
    ### KONIEC ROZWIAZANIA

    f.close()


def subsum(A, x):
    ### POCZATEK ROZWIAZANIA

    if x == 0:
        return True

    if len(A) == 0:
        return False

    kopia = A.copy()
    ostatni = kopia.pop()
    value = x-ostatni
    return subsum(kopia, value) or subsum(kopia, x)

    ### KONIEC ROZWIAZANIA





# 8 elementów
t_start = process_time()
assert subsum([5, 6, 1, -4, 8, -7, 11, -82], 102) == False
print(f"Czas wykonywania funkcji dla  8 elementów wyniósł {process_time() - t_start:12.10f} sekund(y).")

# 16 elementów
t_start = process_time()
assert subsum([5, 6, 1, -4, 8, -7, 11, -82, 12, 98, -11, 27, 1029, 83, 77, -415], 1928) == False
print(f"Czas wykonywania funkcji dla 16 elementów wyniósł {process_time() - t_start:12.10f} sekund(y).")

# 24 elementy
t_start = process_time()
assert subsum([5, 6, 1, -4, 8, -7, 11, -82, 12, 98, -11, 27, 1029, 83, 77, -415, 53, 102, 19, -11, 192, 727, 18, -71], 18327) == False
print(f"Czas wykonywania funkcji dla 24 elementów wyniósł {process_time() - t_start:12.10f} sekund(y).")

### BEGIN HIDDEN TESTS
assert subsum([1, 2, 4, 8, 16, 32, 64], 123) == True
assert subsum([1, 2, 4, 8, 16, 32, 64], 76) == True
assert subsum([2, 4, 8, 16, 21, 64], 96) == False
assert subsum([1, 1, 1, 1, 1, 1, 1], 5) == True
### END HIDDEN TESTS
print("koniec hidden testow")
#
# def subsum(A, x):
#     ### POCZATEK ROZWIAZANIA
#     n = len(A)
#     def isSubsetSum(set, n, sum):
#
#         if sum == 0:
#             return True
#         if n == 0 and sum != 0:
#             return False
#
#
#         if (set[n - 1] > sum):
#             return isSubsetSum(set, n - 1, sum);
#
#         return isSubsetSum(set, n - 1, sum) or isSubsetSum(set, n - 1, sum - set[n - 1])
#
#     value = isSubsetSum(A, n, x)
#     return value
#     ### KONIEC ROZWIAZANIA