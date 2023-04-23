package main

import (
	"encoding/binary"
	"flag"
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

var devicecNameFlag = flag.String("device", "none", "device name")

func xorCipher(data []byte, seed int, xorKey []byte) {
	for i := 0; i < len(data); i++ {
		data[i] ^= xorKey[seed%len(xorKey)]
		seed++
	}
}

func selectInterface() string {
	interfaces, err := pcap.FindAllDevs()

	if err != nil {
		panic(err)
	}

	for i, iface := range interfaces {
		println(i, iface.Name)
	}

	var selected int

	println("Select interface: ")

	_, err = fmt.Scanf("%d", &selected)

	if err != nil {
		panic(err)
	}

	return interfaces[selected].Name
}

func sniffer(processPacket func([]byte)) {
	var interfaceName string

	if *devicecNameFlag == "none" {
		interfaceName = selectInterface()
	} else {
		interfaceName = *devicecNameFlag
	}

	println("Starting sniffer on interface: ", interfaceName)

	handle, err := pcap.OpenLive(interfaceName, 65536, false, 3)

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

		if packet.ApplicationLayer() == nil {
			continue
		}

		processPacket(packet.ApplicationLayer().Payload())
	}

}

func processPacket(raw []byte) {

	AuctionSearchOpCode := 36394

	packet_size := binary.LittleEndian.Uint16(raw[0:2])
	op_code := binary.LittleEndian.Uint16(raw[2:4])

	if int(op_code) != AuctionSearchOpCode {
		return
	}

	xorCipher(raw[6:packet_size], int(op_code), xor_key)

	decompressed, err := oodle.Decompress(raw[6:packet_size])

	if err != nil {
		panic(err)
	}

	parser.ParseData(decompressed)

}

// Decompresses a byte array of Oodle Compressed Data (Requires Oodle DLL)
func main() {
	flag.Parse()

	oodle.Init()
	sniffer(processPacket)
}

// func old() {

// rawData, err := ioutil.ReadFile("D:/projects/market-parser/raw.bin")

// if err != nil {
// 	panic(err)
// }
// 	handle, err := pcap.OpenLive("\\Device\\NPF_{BF46F36F-F80E-4E9D-8D8A-18A8C353858E}", 65536, false, 3)

// 	if err != nil {
// 		panic(err)
// 	}

// 	filter := "tcp src port 6040"
// 	err = handle.SetBPFFilter(filter)
// 	if err != nil {
// 		panic(err)
// 	}

// 	packetSource := gopacket.NewPacketSource(handle, handle.LinkType())

// 	// for packet := range packetSource.Packets() {
// 	// 	// processPacket(packet)
// 	// }
// }
