from ortools.sat.python import cp_model
import json
from typing_extensions import TypedDict
from typing import List, Literal, Callable, Tuple, Set
from functools import reduce
from tabulate import tabulate, SEPARATING_LINE
import numpy as np
import csv

STONE: List[Tuple[str, int]] = [("Hit Master", 7), ("Adrenaline", 7)]
BOOK: List[Tuple[str, int]] = [("Grudge", 12), ("Igniter", 12)]

ENGRAVING_CHOICES = [('Precise Dagger', 15), ("AllOutAttack", 15)]
STATUS_REQUESTED = ["Spec", "Crit"]
MAIN_STATUS = 'Spec'
ONLY_BUY_NOW = False
ONLY_BID = False
MAX_VALUE = 0


class Status(TypedDict):
    StatusType: Literal['Swiftness', 'Spec', 'lazy add the rest later']
    StatusValue: int

class Engravings(TypedDict):
    EngravingType: str
    Value: int

class Accessory(TypedDict):
    Buyout: int
    Bid: int
    Id: str
    Status: List[Status]
    Type: Literal['ring', 'earring', 'necklace']
    Engravings: List[Engravings]


with open('dataset.json', 'r') as dataset:
    data: List[Accessory] = json.load(dataset)
    necklaces: List[Accessory] = []
    earrings: List[Accessory] = []
    rings: List[Accessory] = []

    for item in data:
        
        # if item['Type'] == 'necklace':
        #     for item_status in item['Status']:
        #         if item_status['StatusType'] not in STATUS_REQUESTED:
        #             continue
        # else:
        #     if item['Status'][0]['StatusType'] != MAIN_STATUS:
        #         continue
            
        # normalized_accessory_engraving = list(map(lambda x: x['EngravingType'], item['Engravings']))
        # normalized_chosen_engraving = list(map(lambda x: x[0], ENGRAVING_CHOICES))
        
        # if True not in np.in1d(normalized_accessory_engraving, normalized_chosen_engraving): continue

        if ONLY_BUY_NOW and not item['Buyout']: continue
        if item['Type'] == 'ring':
            rings.append(item)
        elif item['Type'] == 'earring':
            earrings.append(item)
        else:
            necklaces.append(item)
            

necklaceIntVars = []
earringsIntVars = []
ringsIntVars = []

model = cp_model.CpModel()

def search(accessory: Accessory, engravingType: str, cost = 0) -> int:
    for engraving in accessory['Engravings']:
        if engraving['EngravingType'] == engravingType:
            return engraving['Value']
    
    return 0


for i, _ in enumerate(necklaces):
    necklaceIntVars.append(model.NewIntVar(0, 1, f'necklace{i}'))

for i, _ in enumerate(earrings):
    earringsIntVars.append(model.NewIntVar(0, 1, f'earring{i}'))

for i, _ in enumerate(rings):
    ringsIntVars.append(model.NewIntVar(0, 1, f'ring{i}'))


model.Add(cp_model.LinearExpr.Sum(necklaceIntVars) == 1)
model.Add(cp_model.LinearExpr.Sum(earringsIntVars) == 2)
model.Add(cp_model.LinearExpr.Sum(ringsIntVars) == 2)



def GetSumOfEngravingType(engravingType: str):
    linearExpr = []
    for i, _ in enumerate(necklaces):
        linearExpr.append(necklaceIntVars[i] * search(necklaces[i], engravingType))

    for i, _ in enumerate(earrings):
        linearExpr.append(earringsIntVars[i] * search(earrings[i], engravingType))

    for i, _ in enumerate(rings):
        linearExpr.append(ringsIntVars[i] * search(rings[i], engravingType))
        
    
    return cp_model.LinearExpr.Sum(linearExpr)


def getBuyoutOrBidValue(accessory: Accessory):
    return accessory['Buyout'] if accessory['Buyout'] else accessory['Bid']

def GetSumOfCost():
    linearExpr = []
    for i, _ in enumerate(necklaces):
        linearExpr.append(necklaceIntVars[i] * getBuyoutOrBidValue(necklaces[i]))

    for i, _ in enumerate(earrings):
        linearExpr.append(earringsIntVars[i] * getBuyoutOrBidValue(earrings[i]))

    for i, _ in enumerate(rings):
        linearExpr.append(ringsIntVars[i] * getBuyoutOrBidValue(rings[i]))
    
    return cp_model.LinearExpr.Sum(linearExpr)



def find_stone_or_book(engraving: str) -> int:
    if STONE:
        for name, value in STONE:
            if engraving == name:
                return value
    if BOOK:
        for name, value in BOOK:
            if engraving == name:
                return value
    
    return 0

for desiredEngraving in ENGRAVING_CHOICES:
    name, value = desiredEngraving
    model.Add(GetSumOfEngravingType(name) >= (value - find_stone_or_book(name)))
    




# if MAX_VALUE:
#     model.Add(GetSumOfCost() <= MAX_VALUE)

solver = cp_model.CpSolver()


permutations: List[List[Accessory]] = []

class MySolutionCallback(cp_model.CpSolverSolutionCallback):

    def __init__(self):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.accessories = []
        self.accessories.extend(necklaces)
        self.accessories.extend(earrings)
        self.accessories.extend(rings)

    def on_solution_callback(self):
        solution = self.Response().solution
        # if self.Response().status != cp_model.OPTIMAL: return;
        build = []
        for i, result in enumerate(solution):
            if result: build.append(self.accessories[i])

        
        permutations.append(build)
        
solver.parameters.enumerate_all_solutions = True
# if you want less solution decrase the max time in seconds or it will take forever
solver.parameters.max_time_in_seconds = 2
solver.parameters.log_search_progress = True
solver.log_callback = print

solver.Solve(model, MySolutionCallback())


def accumulator(acc: int, permutation: Accessory):
    if ONLY_BID:
        return acc + permutation['Bid']
    return acc + permutation['Buyout'] if permutation['Buyout'] else permutation['Bid']

print("Number of avaiable builds", len(permutations))



headers = ['Bid', 'Buy now']
for status in STATUS_REQUESTED:
    headers.append(status)

for engraving in ENGRAVING_CHOICES:
    headers.append(engraving[0])

table = [headers]

done_ids: Set[str] = set()

for i, permutation in enumerate(permutations, 1):
    total_cost_bid_only = 0
    total_cost_buy_now = 0
    total_cost_mixed = 0
    ids: List[str] = []
    
    for item in permutation:
        bid = item['Bid'] if item['Bid'] else 0
        buy_now = item['Buyout'] if item['Buyout'] else 0
        total_cost_bid_only += bid
        total_cost_buy_now += buy_now
        total_cost_mixed += bid if bid > 0 else buy_now
        row = [bid, buy_now]
        row.extend([0]*len(STATUS_REQUESTED))
        row.extend([0]*len(ENGRAVING_CHOICES))
        ids.append(item['Id'])

        for status in item['Status']:
            if status['StatusType'] in STATUS_REQUESTED:
                indexof = STATUS_REQUESTED.index(status['StatusType'])
                row[indexof + 2] = status['StatusValue']

        for engraving in item['Engravings']:
            if engraving['EngravingType'] in headers:
                row[headers.index(engraving['EngravingType'])] = engraving['Value']
        
        table.append(row)

    ids.sort()

    sum_id = ''.join(ids)

    if sum_id in done_ids:
        print('REPETIDO', sum_id)
    done_ids.add(sum_id)

    table.append(headers)
    
    
print(tabulate(table, tablefmt='grid'))
    

with open('results.csv', 'w', newline='') as f:
    write = csv.writer(f)
    for row in table:
        write.writerow(row)
    









