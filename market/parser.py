import struct

OFFSETS = {
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

class MarketParser:
    def __init__(self, data: bytearray) -> None:
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

        self.search_results = []

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

    def _get_item_header(self, offset):

        header = {
            "item_id": struct.unpack_from('<i', self.data, offset + OFFSETS['ITEM_ID'])[0],
        }

        if header['item_id'] in EARRINGS:
            header['type'] = 'earring'
        elif header['item_id'] in RINGS:
            header['type'] = 'ring'
        elif header['item_id'] in NECKLACES:
            header['type'] = 'necklace'
        
        if header['type'] == 'necklace':
            header['buyout'] = struct.unpack_from('<i', self.data, offset + OFFSETS['NECKLACE']['BUYOUT'])[0]
            header['bid'] = struct.unpack_from('<i', self.data, offset + OFFSETS['NECKLACE']['BID'])[0]
        elif header['type'] == 'earring' or header['type'] == 'ring':
            header['buyout'] = struct.unpack_from('<i', self.data, offset + OFFSETS['RING']['BUYOUT'])[0]
            header['bid'] = struct.unpack_from('<i', self.data, offset + OFFSETS['RING']['BID'])[0]

        return header
    
    def _get_necklace_status(self, offset):
        buyout_offset = offset + OFFSETS['NECKLACE']['BUYOUT']
        bid_offset = offset + OFFSETS['NECKLACE']['BID']
        stat1_offset = offset + OFFSETS['NECKLACE']['STAT1']
        stat2_offset = offset + OFFSETS['NECKLACE']['STAT2']
        neg_offset = offset + OFFSETS['NECKLACE']['NEG']
        eng1_offset = offset + OFFSETS['NECKLACE']['ENG1']
        eng2_offset = offset + OFFSETS['NECKLACE']['ENG2']

        return {
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
            "buyout": struct.unpack_from('<i', self.data, buyout_offset)[0],
            "bid": struct.unpack_from('<i', self.data, bid_offset)[0]        
        }
    
    def _get_ring_earring_status(self, offset):
        buyout_offset = offset + OFFSETS['RING']['BUYOUT']
        bid_offset = offset + OFFSETS['RING']['BID']
        stat1_offset = offset + OFFSETS['RING']['STAT1']
        eng1_offset = offset + OFFSETS['RING']['ENG1']
        eng2_offset = offset + OFFSETS['RING']['ENG2']
        neg_offset = offset + OFFSETS['RING']['NEG']

        print(offset)

        return {
            "stat1": struct.unpack_from('<i', self.data, stat1_offset)[0],
            "stat1_value": struct.unpack_from('<i', self.data, stat1_offset+OFFSETS['VALUE_OFFSET'])[0],
            "neg": struct.unpack_from('<i', self.data, neg_offset)[0],
            "neg_value": struct.unpack_from('<i', self.data, neg_offset+OFFSETS['VALUE_OFFSET'])[0],
            "eng1": struct.unpack_from('<i', self.data, eng1_offset)[0],
            "eng1_value": struct.unpack_from('<i', self.data, eng1_offset+OFFSETS['VALUE_OFFSET'])[0],
            "eng2": struct.unpack_from('<i', self.data, eng2_offset)[0],
            "eng2_value": struct.unpack_from('<i', self.data, eng2_offset+OFFSETS['VALUE_OFFSET'])[0],
            "buyout": struct.unpack_from('<i', self.data, buyout_offset)[0],
            "bid": struct.unpack_from('<i', self.data, bid_offset)[0]
        }
    
    def parse(self):


        current_offset = 0
        for _ in range(self.search_header_value['total_items']):
            item_header = self._get_item_header(current_offset)

            if item_header['item_id'] in NECKLACES:
                item_status = self._get_necklace_status(current_offset)
                current_offset += self.item_header_size + self.necklace_footer_size
            elif item_header['item_id'] in RINGS or item_header['item_id'] in EARRINGS:
                item_status = self._get_ring_earring_status(current_offset)
                current_offset += self.item_header_size + self.earring_ring_footer_size

            result = {}

            result['item_id'] = item_header['item_id']
            result['type'] = item_header['type']
            result['buyout'] = item_header['buyout']
            result['bid'] = item_header['bid']
            result['item_status'] = item_status

            self.search_results.append(result)
            


if __name__ == '__main__':
    rings = open('necklace-crit-exprt.bin', 'rb').read()

    parser = MarketParser(rings)

    parser.parse()

    for item in parser.search_results:
        print(item)

        
        