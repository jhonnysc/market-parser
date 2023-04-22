package main

import (
	"encoding/binary"
	"fmt"
	"io/ioutil"
	oodle "market/oodle"
	parser "market/packet/market_search"

	"github.com/google/gopacket"
	"github.com/google/gopacket/pcap"
)

var (
	xor_key, _ = ioutil.ReadFile("../meter-data/xor.bin")
)

func xor_cipher(data []byte, seed int, xorKey []byte) {
	for i := 0; i < len(data); i++ {
		data[i] ^= xorKey[seed%len(xorKey)]
		seed++
	}
}

// Decompresses a byte array of Oodle Compressed Data (Requires Oodle DLL)
func main() {

	rawData, err := ioutil.ReadFile("D:/projects/market-parser/raw.bin")

	if err != nil {
		panic(err)
	}

	oodle.Init()

	packet_size := binary.LittleEndian.Uint16(rawData[0:2])
	op_code := binary.LittleEndian.Uint16(rawData[2:4])

	AuctionSearchOpCode := 36394

	if int(op_code) != AuctionSearchOpCode {
		return
	}

	xor_cipher(rawData[6:packet_size], int(op_code), xor_key)

	decompressed, err := oodle.Decompress(rawData[6:packet_size])

	if err != nil {
		panic(err)
	}

	parser.ParseData(decompressed)

	// search := decompressed[16:]

	// fmt.Printf("val1: %d\n", binary.LittleEndian.Uint32(search[99:]))
	// fmt.Printf("val2: %d\n", binary.LittleEndian.Uint32(search[99+17:]))

}

func old() {
	handle, err := pcap.OpenLive("\\Device\\NPF_{BF46F36F-F80E-4E9D-8D8A-18A8C353858E}", 65536, false, 3)

	if err != nil {
		panic(err)
	}

	filter := "tcp src port 6040"
	err = handle.SetBPFFilter(filter)
	if err != nil {
		panic(err)
	}

	packetSource := gopacket.NewPacketSource(handle, handle.LinkType())

	for packet := range packetSource.Packets() {
		processPacket(packet)
	}
}

func processPacket(packet gopacket.Packet) {

	rawLayer := packet.ApplicationLayer().Payload()

	const auctionSearchOpCode = 36394

	var op_code uint16
	// var pkt_size uint16

	// pkt_size = binary.BigEndian.Uint16(rawLayer[0:2])
	op_code = binary.BigEndian.Uint16(rawLayer[2:4])

	println(rawLayer[2:4])
	if op_code == auctionSearchOpCode {
		fmt.Printf("Packet")
	}

}
