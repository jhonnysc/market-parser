import struct
from typing import Dict
import json
from uuid import uuid4

with open('Engravings.json', 'r') as r:
    STATS: Dict = json.load(r)

# tuple 400, 460, 18, 456, 15, 500, 1, 802, 3, 199, 4, 3, 248
def parse_necklace(data: tuple, buyout: int, bid: int) -> Dict:
    return {
        "Status": [
            {
                "StatusType": STATS.get(str(data[2]), data[2]),
                "StatusValue": data[1]
            },
            {
                "StatusType":  STATS.get(str(data[4]), data[4]),
                "StatusValue": data[3]
            }
        ],
        "Id": str(uuid4()),
        "Buyout": buyout,
        "Bid": bid,
        "Type": "necklace",
        "Engravings": [
            {
                "EngravingType": STATS.get(str(data[7]), data[7]),
                "Value": data[6]
            },
            {
                "EngravingType": STATS.get(str(data[9]), data[9]),
                "Value": data[8]
            },
            {
                "EngravingType": STATS.get(str(data[12]), data[12]),
                "Value": data[11]
            }
        ]
    }    

def parse_ring_earring(data: tuple, buyout: int, bid: int, item_id) -> Dict:
    return {
        "Status": [
            {
                "StatusType": STATS.get(str(data[2]), data[2]),
                "StatusValue": data[1]
            },
        ],
        "Id": str(uuid4()),
        "Buyout": buyout,
        "Bid": bid,
        "Type": 'ring' if item_id in RINGS else 'earring',
         "Engravings": [
            {
                "EngravingType": STATS.get(str(data[5]), data[5]),
                "Value": data[4]
            },
            {
                "EngravingType": STATS.get(str(data[9]), data[9]),
                "Value": data[8]
            },
            {
                "EngravingType": STATS.get(str(data[11]), data[11]),
                "Value": data[10]
            }
        ]
    }    


def print_search_result(search: bytes) -> None:
    print(search)
    _, _, count = SEARCH_HEADER.unpack_from(search, 0)
    offset = SEARCH_HEADER.size
    print(offset)
    print( + NECKLACE_FOOTER.size)
    results = []
    for _ in range(count):
        _, _, buyout, bid, item_id = ITEM_HEADER.unpack_from(search, offset)
        offset += ITEM_HEADER.size
        if item_id in EARINGS or item_id in RINGS:
            results.append(parse_ring_earring(EARING_FOOTER.unpack_from(search, offset), buyout, bid, item_id))
            offset += EARING_FOOTER.size
        if item_id in NECKLACES:
            results.append(parse_necklace(NECKLACE_FOOTER.unpack_from(search, offset), buyout, bid))
            offset += NECKLACE_FOOTER.size
    
    with open('dataset.json', 'r+') as d:
        js: list = json.load(d)

        js.extend(results)

        d.seek(0)
        d.write(json.dumps(js, indent=4))
        d.truncate()



def create_struct(template: str) -> struct.Struct:
    return struct.Struct(template.replace(4 * 'i', 'i').replace(8 * 'q', 'q'))

SEARCH_HEADER = create_struct('<'
    'iiiiiiiiiiiixx'   # 000 # current_page, max_page, per_this_page
)

ITEM_HEADER = create_struct('<'
    'xxxxiiiixxxxqqqq' # 000 # starting_bid, date
    'qqqqiiiixxxxxxxx' # 010 # buyout
    'xxxxxxxxxxxxxxxx' # 020 #
    'xxxxxiiiixxxxxxx' # 030 # highest_bid
    'xxxxxxxxxxxiiiix' # 040 # item_id
    'xxxxxxxxxxxxxxxx' # 050 #
    'xxxxxxxxxxxxxxxx' # 060 #
    'xxxxxxxxxxxxxxxx' # 070 #
    'xxxxxxxxxxxxxxxx' # 080 #
)

NECKLACE_FOOTER = create_struct('<'
    'xxxxxxxxxxxxxiii' # 090 # stat_min 0
    'ixiiiiiiiixxxxxx' # 0A0 # stat2value 1, stat2type 2 
    'xxxxxxxxxxxxxxxi' # 0B0 # stat1value 3
    'iiiiiiixxxxiiiix' # 0C0 # stat1type 4 , stat_max 5  
    'xxxxxxxxxxxxiiii' # 0D0 # eng3value 6
    'iiiixxxxxxxxxxxx' # 0E0 # eng3type 7
    'xxxxxxxxxiiiiiii' # 0F0 # eng1value 8, eng1type 9
    'ixxxxxxxxxxxxxbx' # 100 # trades_left 10
    'xxxxxxiiiiiiiixx' # 110 # eng2value 11, eng2type 12
    'xxxxxxxxxxxxxxx' # 120 13 #
)

EARING_FOOTER = create_struct('<'
    'xxxxxxxxxxxxxiii' # 090 # stat_min 0
    'ixiiiiiiiixxxxii' # 0A0 # stat_value 1, stat_type 2
    'iixxxxxxxxxxxxxi' # 0B0 # stat_max 3, eng3value 4
    'iiiiiiixxxxiiiix' # 0C0 # eng3type 5, stat_max 6   
    'xxxbxxxxxxxxiiii' # 0D0 # trades_left 7, eng1value 8
    'iiiixxxxxxxxxxxx' # 0E0 # eng1type 9
    'xxxxxxxxxiiiiiii' # 0F0 # eng2value 10, eng2type 11
    'ixxxxxxxxxxxxxxx' # 100 12#
    'xx'              # 110 13 #
)

EARINGS = {
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
}

RINGS = {
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
}

NECKLACES = {
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
}

