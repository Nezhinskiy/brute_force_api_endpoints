from itertools import product, permutations

run = True
def get_api_answer(world):
    if world == 'sdf':
        print('!!!!!!!', world)

def ppermutations(iterable, length):
    pool = tuple(iterable)
    n = len(pool)
    r = length
    c = []
    for indices in product(range(n), repeat=r):
        if len(set(indices)) == r:
            get_api_answer(''.join((pool[i]) for i in indices))
            c.append(''.join((pool[i]) for i in indices))
    print(len(c))
    print(len(set(c)))



iterable = 'abcdefghijklmnopqrstuvwxyz1234567890'
length = 4
# a = ppermutations(iterable, length)
# print(len(a))
iterable = 'etaoinshrdlcumwfgypbvkjxqz'
length = 1
print(len(set(permutations(iterable, length))))
#с цифрами
# 2 = 1260
# 3 = 42840
# 4 = 1413720

# без цифр
# 2 = 650
# 3 = 15600
# 4 = 358800