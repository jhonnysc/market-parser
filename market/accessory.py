import struct


def print_search_result(search: bytes) -> None:
    _, _, count = SEARCH_HEADER.unpack_from(search, 0)
    offset = SEARCH_HEADER.size
    print( + NECKLACE_FOOTER.size)
    for _ in range(count):
        _, _, buyout, bid, item_id = ITEM_HEADER.unpack_from(search, offset)
        offset += ITEM_HEADER.size
        if item_id in EARINGS:
            print(*EARING_FOOTER.unpack_from(search, offset))
            offset += EARING_FOOTER.size
        if item_id in NECKLACES:
            print(*NECKLACE_FOOTER.unpack_from(search, offset))
            offset += NECKLACE_FOOTER.size

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
    'xxxxxxxxxxxxxiii' # 090 # stat_min
    'ixiiiiiiiixxxxxx' # 0A0 # stat2value, stat2type
    'xxxxxxxxxxxxxxxi' # 0B0 # stat1value
    'iiiiiiixxxxiiiix' # 0C0 # stat1type, stat_max   
    'xxxxxxxxxxxxiiii' # 0D0 # eng3value
    'iiiixxxxxxxxxxxx' # 0E0 # eng3type
    'xxxxxxxxxiiiiiii' # 0F0 # eng1value, eng1type
    'ixxxxxxxxxxxxxbx' # 100 # trades_left
    'xxxxxxiiiiiiiixx' # 110 # eng2value, eng2type
    'xxxxxxxxxxxxxxx' # 120 #
)

EARING_FOOTER = create_struct('<'
    'xxxxxxxxxxxxxiii' # 090 # stat_min
    'ixiiiiiiiixxxxii' # 0A0 # stat_value, stat_type
    'iixxxxxxxxxxxxxi' # 0B0 # stat_max, eng3value
    'iiiiiiixxxxiiiix' # 0C0 # eng3type, stat_max   
    'xxxbxxxxxxxxiiii' # 0D0 # trades_left, eng1value
    'iiiixxxxxxxxxxxx' # 0E0 # eng1type
    'xxxxxxxxxiiiiiii' # 0F0 # eng2value, eng2type
    'ixxxxxxxxxxxxxxx' # 100 #
    'xx'              # 110 #
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

