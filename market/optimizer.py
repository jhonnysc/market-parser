from collections import defaultdict, namedtuple
from enum import Enum, auto

Engraving = namedtuple('Engraving', ['type1', 'value1', 'type2', 'value2'])

class Rarity(Enum):
    Ancient = auto()
    Relic = auto()
    Legendary = auto()

class Type(Enum):
    Necklace = auto()
    Earing = auto()
    Ring = auto()

RANGES = {
    (Rarity.Ancient,):                (range(3, 6 + 1), range(4, 6 + 1)),
    (Rarity.Relic,):                  (range(3, 5 + 1), range(3, 5 + 1)),
    (Rarity.Legendary,):              (range(2, 4 + 1), range(2, 4 + 1)),
    (Rarity.Ancient, Rarity.Relic):   (range(3, 6 + 1), range(3, 6 + 1)),
    (Rarity.Relic, Rarity.Legendary): (range(2, 5 + 1), range(2, 5 + 1)),
}


class BuildFinder:
    def __init__(self, required_values: list[int]) -> None:
        self._required_values: list[int] = required_values
        self._stack: list[Engraving] = []
        self._builds: list[list[Engraving]] = []
        self._candidates = self._generate_candidates(*RANGES[(Rarity.Relic,)])

    def _generate_candidates(self, low_range, high_range) -> list[Engraving]:
        result: list[Engraving] = []
        for value in low_range:
            for type in range(len(self._required_values)):
                result.append(Engraving(0, 0, type, value))
        for value in high_range:
            for type1 in range(len(self._required_values)):
                for type2 in range(len(self._required_values)):
                    if type1 != type2 and (value != 3 or type1 < type2):
                        result.append(Engraving(type1, 3, type2, value))
        return result

    def _dfs_builds(self, index: int) -> None:
        """ similar problem to https://leetcode.com/problems/combination-sum/ """
        if self.is_done():
            self._builds.append(self._stack.copy())
            return
        if index >= len(self._candidates) or len(self._stack) >= 5 or not self.is_possible():
            return

        accessory = self._candidates[index]
        if self._required_values[accessory.type2] > 0 and (self._required_values[accessory.type1] > 0 or accessory.value1 == 0):
            self._stack.append(accessory)
            self._required_values[accessory.type1] -= accessory.value1
            self._required_values[accessory.type2] -= accessory.value2
            self._dfs_builds(index)
            self._stack.pop()
            self._required_values[accessory.type1] += accessory.value1
            self._required_values[accessory.type2] += accessory.value2
        self._dfs_builds(index + 1)

    def get_stats(self) -> None:
        stats: dict[Engraving, int] = defaultdict(int)
        for build in self._builds:
            for acc in build:
                stats[acc] += 1
        print(*sorted(stats.items(), key=lambda x: x[1]), sep='\n')

    def is_possible(self) -> bool:
        required_sum = 0
        required_max = 0
        for value in self._required_values: 
            if value > 0:
                required_sum += max(value, 3)  # TODO: change 3 depening on acc's type
                required_max = max(value, required_max)

        # TODO: change 8 and 5 depening on acc's type
        limit_sum = (5 - len(self._stack)) * 8
        limit_max = (5 - len(self._stack)) * 5
        if required_sum > limit_sum or required_max > limit_max:
            return False
        return True

    def is_done(self) -> bool:
        for value in self._required_values: 
            if value > 0:
                return False
        return True


if __name__ == '__main__':
    # desired = [15, 15, 15, 15, 15]
    # setup   = [12,  9,  9,  7,  0]
    temp = BuildFinder([3, 6, 6, 8, 15])
    temp._dfs_builds(0)

    # Find how many of build are duplicates
    res = set()
    for build in temp._builds:
        res.add(frozenset(build))
    # Should't have any duplicates
    print(len(temp._builds), len(res))


    for build in temp._builds:
        for acc in build:
            print(f'{acc.type1}:{acc.value1} {acc.type2}:{acc.value2}', end=' ')
        print()
    temp.get_stats()