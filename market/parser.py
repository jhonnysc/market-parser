import struct
from dataclasses import dataclass
from typing import List, Literal, Dict, Any

OFFSETS: Dict[str, Any] = {
    "VALUE_OFFSET": 17,
    "ITEM_ID": 26,
    "NECKLACE": {
        "STAT1": 99,
        "STAT2": 128,
        "ENG1": 157,
        "ENG2": 186,
        "BID": 267,
        "BUYOUT": 283,
        "NEG": 157
    },
    "RING": {
        "STAT1": 99,
        "ENG1": 157,
        "ENG2": 186,
        "BID": 238,
        "BUYOUT": 254,
        "NEG": 128
    },
}

EARRINGS = [
    # relic earing

    213300011,
    213300021,
    213300031,
    213300041,
    213300051,
    213300061,
    213300111,
    213300121,
    213300131,
    213300141,
    213300151,
    213300161,

    # legendary earing
    213200061,
    213200051,
    213200021,
    213200011,
    213200031,
    213200041,
]

RINGS = [
    # relic rings
    213300012,
    213300022,
    213300032,
    213300042,
    213300052,
    213300062,
    213300112,
    213300122,
    213300132,
    213300142,
    213300152,
    213300162,
    # legendary rings
    213200062,
    213200052,
    213200022,
    213200012,
    213200032,
    213200042
]

NECKLACES = [
    # relic necklaces
    213300010,
    213300030,
    213300050,
    213300110,
    213300130,
    213300150,
    # legendary necklaces
    213200050,
    213200010,
    213200030,
]

engravings = {
    107: "Disrespect",
    109: "Spirit Absorption",
    110: "Ether Predator",
    111: "Stabilized Status",
    118: "Grudge",
    121: "Super Charge",
    123: "Strong Will",
    125: "Mayhem",
    127: "Esoteric Skill Enhancement",
    129: "Enhanced Weapon",
    130: "Firepower Enhancement",
    134: "Drops of Ether",
    140: "Crisis Evasion",
    141: "Keen Blunt Weapon",
    142: "Vital Point Hit",
    167: "Max MP Increase",
    168: "MP Efficiency Increase",
    188: "Berserker's Technique",
    189: "First Intention",
    190: "Ultimate Skill: Taijutsu",
    191: "Shock Training",
    192: "Pistoleer",
    193: "Barrage Enhancement",
    194: "True Courage",
    195: "Desperate Salvation",
    196: "Rage Hammer",
    197: "Gravity Training",
    198: "Master Summoner",
    199: "Communication Overflow",
    202: "Master of Escape",
    224: "Combat Readiness",
    225: "Lone Knight",
    235: "Fortitude",
    236: "Crushing Fist",
    237: "Shield Piercing",
    238: "Master's Tenacity",
    239: "Divine Protection",
    240: "Heavy Armor",
    241: "Explosive Expert",
    242: "Enhanced Shield",
    243: "Necromancy",
    244: "Preemptive Strike",
    245: "Broken Bone",
    246: "Lightning Fury",
    247: "Cursed Doll",
    248: "Contender",
    249: "Ambush Master",
    251: "Magick Stream",
    253: "Barricade",
    254: "Raid Captain",
    255: "Awakening",
    256: "Energy Overflow",
    257: "Robust Spirit",
    258: "Loyal Companion",
    259: "Death Strike",
    276: "Pinnacle",
    277: "Control",
    278: "Remaining Energy",
    279: "Surge",
    280: "Perfect Suppression",
    281: "Demonic Impulse",
    282: "Judgment",
    283: "Blessed Aura",
    284: "Arthetinean Skill",
    285: "Evolutionary_Legacy",
    288: "Master Brawler",
    289: "Peacemaker",
    290: "Time to Hunt",
    291: "Deathblow",
    292: "Esoteric Flurry",
    293: "Igniter",
    294: "Reflux",
    295: "Increases Mass",
    296: "Propulsion",
    297: "Hit Master",
    298: "Sight Focus",
    299: "Adrenaline",
    300: "All-Out Attack",
    301: "Expert",
    302: "Emergency Rescue",
    303: "Precise Dagger",
    803: "Move Speed Reduction",
    802: "Atk. Speed Reduction",
    801: "Defense Reduction",
    800: "Atk. Power Reduction",
    15: "Crit",
    16: "Spec",
    17: "Domination",
    18: "Swiftness",
    19: "Endurance",
    20: "Expertise"
}


@dataclass
class ItemHeader:
    item_id: int
    item_type: Literal["ring", "earring", "necklace"]
    buyout_price: int
    bid_price: int


@dataclass
class SearchHeader:
    current_page: int
    total_pages: int
    total_items: int


@dataclass
class SearchResults:
    search_header: SearchHeader
    item_headers: List[ItemHeader]


@dataclass
class Engraving:
    engraving_name: str
    engraving_id: int
    engraving_value: int


@dataclass
class Status:
    status_name: str
    status_id: int
    status_value: int


@dataclass
class AccessoryStatus:
    engravings: List[Engraving]
    statuses: List[Status]


@dataclass
class Accessory:
    header: ItemHeader
    footer: AccessoryStatus


class MarketParser:
    def __init__(self, data: bytes) -> None:
        self.data = data
        self.search_header_size = 14
        self.item_header_size = 144
        self.necklace_footer_size = 159
        self.earring_ring_footer_size = 130
        self.pagination_offsets = {
            'current_page': 8,
            'total_pages': 4,
            'total_items': 0
        }

        self.search_header_value = self._get_search_header()

        self.search_results: List[Accessory] = []

    def _get_search_header(self):
        search_header_value = {
            'current_page': struct.unpack_from('<i', self.data, self.pagination_offsets['current_page'])[0]+1,
            'total_pages': struct.unpack_from('<i', self.data, self.pagination_offsets['total_pages'])[0],
        }

        if search_header_value['current_page'] <= search_header_value['total_pages']:
            search_header_value['total_items'] = 10
        else:
            search_header_value['total_items'] = 'idk'

        return search_header_value

    def _get_item_header(self, offset) -> ItemHeader:

        item_id = struct.unpack_from(
            '<i', self.data, offset + OFFSETS['ITEM_ID'])[0]

        item_type: Literal["ring", "earring", "necklace"]

        if item_id in EARRINGS:
            item_type = 'earring'
        elif item_id in RINGS:
            item_type = 'ring'
        elif item_id in NECKLACES:
            item_type = 'necklace'

        if item_type == 'necklace':
            buyout_price = struct.unpack_from(
                '<i', self.data, offset + OFFSETS['NECKLACE']['BUYOUT'])[0]
            bid_price = struct.unpack_from(
                '<i', self.data, offset + OFFSETS['NECKLACE']['BID'])[0]
        elif item_type == 'earring' or item_type == 'ring':
            buyout_price = struct.unpack_from(
                '<i', self.data, offset + OFFSETS['RING']['BUYOUT'])[0]
            bid_price = struct.unpack_from(
                '<i', self.data, offset + OFFSETS['RING']['BID'])[0]

        return ItemHeader(
            item_id=item_id,
            item_type=item_type,
            buyout_price=buyout_price,
            bid_price=bid_price
        )

    def _get_necklace_status(self, offset) -> AccessoryStatus:
        stat1_offset = offset + OFFSETS['NECKLACE']['STAT1']
        stat2_offset = offset + OFFSETS['NECKLACE']['STAT2']
        neg_offset = offset + OFFSETS['NECKLACE']['NEG']
        eng1_offset = offset + OFFSETS['NECKLACE']['ENG1']
        eng2_offset = offset + OFFSETS['NECKLACE']['ENG2']

        raw_status = {
            "stat1": struct.unpack_from('<i', self.data, stat1_offset)[0],
            "stat1_value": struct.unpack_from('<i', self.data, stat1_offset+OFFSETS['VALUE_OFFSET'])[0],
            "stat2": struct.unpack_from('<i', self.data, stat2_offset)[0],
            "stat2_value": struct.unpack_from('<i', self.data, stat2_offset+OFFSETS['VALUE_OFFSET'])[0],
            "neg": struct.unpack_from('<i', self.data, neg_offset)[0],
            "neg_value": struct.unpack_from('<i', self.data, neg_offset+OFFSETS['VALUE_OFFSET'])[0],
            "eng1": struct.unpack_from('<i', self.data, eng1_offset)[0],
            "eng1_value": struct.unpack_from('<i', self.data, eng1_offset+OFFSETS['VALUE_OFFSET'])[0],
            "eng2": struct.unpack_from('<i', self.data, eng2_offset)[0],
            "eng2_value": struct.unpack_from('<i', self.data, eng2_offset+OFFSETS['VALUE_OFFSET'])[0],
        }

        engraving1 = Engraving(
            engraving_name=engravings[raw_status['eng1']],
            engraving_id=raw_status['eng1'],
            engraving_value=raw_status['eng1_value']
        )

        engraving2 = Engraving(
            engraving_name=engravings[raw_status['eng2']],
            engraving_id=raw_status['eng2'],
            engraving_value=raw_status['eng2_value']
        )

        status1 = Status(
            status_name=engravings[raw_status['stat1']],
            status_id=raw_status['stat1'],
            status_value=raw_status['stat1_value']
        )

        status2 = Status(
            status_name=engravings[raw_status['stat2']],
            status_id=raw_status['stat2'],
            status_value=raw_status['stat2_value']
        )

        neg = Status(
            status_name=engravings[raw_status['neg']],
            status_id=raw_status['neg'],
            status_value=raw_status['neg_value']
        )

        return AccessoryStatus(
            engravings=[engraving1, engraving2],
            statuses=[status1, status2, neg],
        )

    def _get_ring_earring_status(self, offset):
        stat1_offset = offset + OFFSETS['RING']['STAT1']
        eng1_offset = offset + OFFSETS['RING']['ENG1']
        eng2_offset = offset + OFFSETS['RING']['ENG2']
        neg_offset = offset + OFFSETS['RING']['NEG']

        raw_data = {
            "stat1": struct.unpack_from('<i', self.data, stat1_offset)[0],
            "stat1_value": struct.unpack_from('<i', self.data, stat1_offset+OFFSETS['VALUE_OFFSET'])[0],
            "neg": struct.unpack_from('<i', self.data, neg_offset)[0],
            "neg_value": struct.unpack_from('<i', self.data, neg_offset+OFFSETS['VALUE_OFFSET'])[0],
            "eng1": struct.unpack_from('<i', self.data, eng1_offset)[0],
            "eng1_value": struct.unpack_from('<i', self.data, eng1_offset+OFFSETS['VALUE_OFFSET'])[0],
            "eng2": struct.unpack_from('<i', self.data, eng2_offset)[0],
            "eng2_value": struct.unpack_from('<i', self.data, eng2_offset+OFFSETS['VALUE_OFFSET'])[0],
        }

        engraving1 = Engraving(
            engraving_name=engravings.get(raw_data['eng1'], 'Unknown'),
            engraving_id=raw_data['eng1'],
            engraving_value=raw_data['eng1_value']
        )

        engraving2 = Engraving(
            engraving_name=engravings.get(raw_data['eng2'], 'Unknown'),
            engraving_id=raw_data['eng2'],
            engraving_value=raw_data['eng2_value']
        )

        status1 = Status(
            status_name=engravings.get(raw_data['stat1'], 'Unknown'),
            status_id=raw_data['stat1'],
            status_value=raw_data['stat1_value']
        )

        neg = Status(
            status_name=engravings.get(raw_data['neg'], 'Unknown'),
            status_id=raw_data['neg'],
            status_value=raw_data['neg_value']
        )

        return AccessoryStatus(
            engravings=[engraving1, engraving2],
            statuses=[status1, neg],
        )

    def _convert_engrave_id_to_name(self, engrave_id):
        return engravings[engrave_id]

    def parse(self):

        current_offset = 0
        for _ in range(self.search_header_value['total_items']):
            item_header = self._get_item_header(current_offset)

            if item_header.item_type == 'necklace':
                item_status = self._get_necklace_status(current_offset)
                current_offset += self.item_header_size + self.necklace_footer_size
            elif item_header.item_type == 'ring' or item_header.item_type == 'earring':
                item_status = self._get_ring_earring_status(current_offset)
                current_offset += self.item_header_size + self.earring_ring_footer_size

            self.search_results.append(Accessory(
                footer=item_status,
                header=item_header
            ))


if __name__ == '__main__':
    rings = open('rings.bin', 'rb').read()

    parser = MarketParser(rings)

    parser.parse()

    for item in parser.search_results:
        print(item)
