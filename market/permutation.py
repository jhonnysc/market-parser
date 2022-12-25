from ortools.sat.python import cp_model
from ortools.sat.python import swig_helper 
import json
from typing_extensions import TypedDict
from typing import List, Literal, Callable
from functools import reduce


ENGRAVING_CHOICES = ['Hit Master', 'Communication Overflow']
ONLY_BUY_NOW = True
ONLY_BID = True
MAX_VALUE = 0


class Status(TypedDict):
    StatusType: Literal['Swiftness', 'Specializaiton', 'lazy add the rest later']
    StatusValue: int

class Engravings(TypedDict):
    EngravingType: str
    Value: int

class Accessory(TypedDict):
    Buyout: int
    Bid: int
    Status: Status
    Type: Literal['ring', 'earring', 'necklace']
    Engravings: List[Engravings]


with open('dataset.json', 'r') as dataset:
    data: List[Accessory] = json.load(dataset)
    necklaces: List[Accessory] = []
    earrings: List[Accessory] = []
    rings: List[Accessory] = []

    for item in data:
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



def search(engravings: List[Engravings], engravingType: str, cost = 0) -> int:
    for engraving in engravings:
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
        linearExpr.append(necklaceIntVars[i] * search(necklaces[i]['Engravings'], engravingType))

    for i, _ in enumerate(earrings):
        linearExpr.append(earringsIntVars[i] * search(earrings[i]['Engravings'], engravingType))

    for i, _ in enumerate(rings):
        linearExpr.append(ringsIntVars[i] * search(rings[i]['Engravings'], engravingType))
    
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

# for desiredEngraving in ENGRAVING_CHOICES:
    # model.Add(GetSumOfEngravingType(desiredEngraving) >= 15)
model.Add(GetSumOfEngravingType('Hit Master') <= 9)
model.Add(GetSumOfEngravingType('Grudge') <= 3)
model.Add(GetSumOfEngravingType('Communication Overflow') <= 9)
model.Add(GetSumOfEngravingType('Raid Captain') <= 15)


if MAX_VALUE:
    model.Add(GetSumOfCost() <= MAX_VALUE)
    
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

solver.Solve(model, MySolutionCallback())

def accumulator(acc: int, permutation: Accessory):
    return acc + permutation['Bid']

price = reduce(accumulator, permutations[0], 0)

print("Number of avaiable builds", len(permutations))








