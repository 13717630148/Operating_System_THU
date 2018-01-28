from random import random

with open('Randoms.txt', 'w') as f:
    for k in range(int(1e6)):
        print('{:6f}'.format(random()), file = f)