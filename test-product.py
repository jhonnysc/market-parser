import json
from itertools import product
import time
from typing import List, Literal, Callable, Tuple, Set


t1 = time.perf_counter()


status_wanted = ['Crit', 'Swift']
engravings_wanted = ['Communication Overflow', 'Grudge', 'Cursed Doll', 'Raid Captain']


def check_stats(d):
    status = d['Status']
    engravings = d['Engravings']

    status_ok, engraving_ok =  False, False

    for s in status:
        if s['StatusType'] in status_wanted:
            status_ok = True
    
    for e in engravings:
        if e['EngravingType'] in engravings_wanted:
            engraving_ok = True

    return status_ok and engraving_ok

with open('./dataset.json', 'r') as f:
    data = json.loads(f.read())

    data = list(filter(check_stats, data))

    # data = [d for d in data if]



necklaces = [d for d in data if d['Type'] == 'necklace']
earrings = [d for d in data if d['Type'] == 'earring']
rings = [d for d in data if d['Type'] == 'ring']


necklaces_index = [i for i, _ in enumerate(necklaces)]
earrings_index = [i for i, _ in enumerate(earrings, len(necklaces))]
rings_index = [i for i, _ in enumerate(rings, len(necklaces) + len(earrings))]

print(necklaces_index[0], earrings_index[0], rings_index[0])




builds = []

progress = 0

for necklace in necklaces_index:
    for ring_a in rings_index:
        for ring_b in rings_index:            
            builds.append([necklace, ring_a, ring_b, None, None])




for b, build in enumerate(builds):
    for earring_a in earrings_index:
        for earring_b in earrings_index:
            progress +=1

            if not progress % 10000000: print(progress, b, earring_a, earring_b)
            build[3], build[4] = earring_a, earring_b

# necklace_ring_product = product()

# STONE: List[Tuple[str, int]] = [("Hit Master", 7), ("Adrenaline", 7)]
# BOOK: List[Tuple[str, int]] = [("Grudge", 12), ("Igniter", 12)]

# ENGRAVING_CHOICES = [('Precise Dagger', 15), ("AllOutAttack", 15)]
# STATUS_REQUESTED = ["Spec", "Crit"]

    # c+=1
    # if c % 100000000 == 0: print(c, end='\r')


# print(earrings_product)

t2 = time.perf_counter()


print('done', t2-t1)