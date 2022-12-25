import time
from scapy.all import AsyncSniffer, Packet, Raw
from pathlib import Path
import struct

from oodle import oodle
from accessory import print_search_result

# TODO: find this somewhere in assets?
AuctionSearchOpCode = 53341

with open(Path('assets', 'xor.bin'), 'rb') as f:
    xorkey = f.read()

def process_packet(packet: Packet):
    if not Raw in packet:
        return 
    p: bytes = packet[Raw].load

    pkt_size, op_code = struct.unpack_from('HH', p)

    if pkt_size > len(p):
        print(f'Fragmented packet {pkt_size}/{len(p)}')
        print(p)

    if not op_code == AuctionSearchOpCode:
        return

    payload_decrypted = xor_cipher(p[6:pkt_size], op_code, xorkey)
    match p[4]:
        case 0: # None
            payload_decrypted = payload_decrypted[16:]
        case 1 | 2: # TODO: L4Z and Snappy
            raise RuntimeError('L4Z and Snappy')
        case 3: # Oodle
            payload_decrypted = oodle.decompress(payload_decrypted)[16:]
        case _: # ?????
            raise RuntimeError('Unknow compression')

    print(f'Packet Size: {pkt_size}/{len(p)}')
    print(f'Commpressed by {p[4]}')
    try:
        print_search_result(payload_decrypted)
    except Exception as e:
        print(e)


# TODO: replace with fast Cython function
def xor_cipher(data: bytes, seed: int, key: bytes) -> bytes:
    decrypted_data = []
    for byte in data:
        decrypted_data.append(byte ^ key[seed % len(key)])
        seed += 1
    return bytes(decrypted_data)


t = AsyncSniffer(filter='tcp src port 6040', prn=process_packet, store=0)
t.start()
time.sleep(600)
t.stop()