package market

import (
	"encoding/binary"
)

var (
	item_header_size         = 144
	search_header_size       = 14
	necklace_footer_size     = 159
	earring_ring_footer_size = 130
)

var EarringsIds = map[uint32]struct{}{
	213400011: {},
	213400021: {},
	213400031: {},
	213400041: {},
	213400051: {},
	213400061: {},
	// relic earing
	213300011: {},
	213300021: {},
	213300031: {},
	213300041: {},
	213300051: {},
	213300061: {},
	213300111: {},
	213300121: {},
	213300131: {},
	213300141: {},
	213300151: {},
	213300161: {},
	// legendary earing
	213200061: {},
	213200051: {},
	213200021: {},
	213200011: {},
	213200031: {},
	213200041: {},
	213200111: {},
}

var RingsIds = map[uint32]struct{}{
	// ancient rings
	213400012: {},
	213400022: {},
	213400032: {},
	213400042: {},
	213400052: {},
	213400062: {},
	// relic rings
	213300012: {},
	213300022: {},
	213300032: {},
	213300042: {},
	213300052: {},
	213300062: {},
	213300112: {},
	213300122: {},
	213300132: {},
	213300142: {},
	213300152: {},
	213300162: {},
	// legendary rings
	213200062: {},
	213200052: {},
	213200022: {},
	213200012: {},
	213200032: {},
	213200042: {},
}

var NecklacesIds = map[uint32]struct{}{
	// ancient necklaces
	213400010: {},
	213400030: {},
	213400050: {},
	// relic necklaces
	213300010: {},
	213300030: {},
	213300050: {},
	213300110: {},
	213300130: {},
	213300150: {},
	// legendary necklaces
	213200050: {},
	213200010: {},
	213200030: {},
}

var StatusIds = map[int]string{
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
	286: "Artist1",
	287: "Artist2",
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
	15:  "Crit",
	16:  "Spec",
	17:  "Domination",
	18:  "Swiftness",
	19:  "Endurance",
	20:  "Expertise",
}

type Necklace struct {
	stat1  uint32
	stat2  uint32
	eng1   uint32
	eng2   uint32
	neg    uint32
	bid    uint32
	buyout uint32
}

type EarringRing struct {
	stat1  uint32
	stat2  uint32
	eng1   uint32
	eng2   uint32
	neg    uint32
	bid    uint32
	buyout uint32
}

type Header struct {
	buyout    uint32
	bid       uint32
	item_type string
	item_id   uint32
}

func GetNecklace(data []byte) Necklace {
	return Necklace{
		stat1:  binary.LittleEndian.Uint32(data[99:]),
		stat2:  binary.LittleEndian.Uint32(data[128:]),
		eng1:   binary.LittleEndian.Uint32(data[215:]),
		eng2:   binary.LittleEndian.Uint32(data[186:]),
		neg:    binary.LittleEndian.Uint32(data[157:]),
		bid:    binary.LittleEndian.Uint32(data[267:]),
		buyout: binary.LittleEndian.Uint32(data[283:]),
	}
}

func GetEarringRing(data []byte) EarringRing {
	return EarringRing{
		stat1:  binary.LittleEndian.Uint32(data[99:]),
		eng1:   binary.LittleEndian.Uint32(data[157:]),
		eng2:   binary.LittleEndian.Uint32(data[186:]),
		neg:    binary.LittleEndian.Uint32(data[128:]),
		bid:    binary.LittleEndian.Uint32(data[238:]),
		buyout: binary.LittleEndian.Uint32(data[254:]),
	}
}

func getHeader(data []byte) Header {
	item_id := binary.LittleEndian.Uint32(data[26:])

	var item_type string

	_, ok := RingsIds[item_id]
	if ok {
		item_type = "Ring"
	}

	_, ok = EarringsIds[item_id]
	if ok {
		item_type = "Earring"
	}

	_, ok = NecklacesIds[item_id]
	if ok {
		item_type = "Necklace"
	}

	if item_type == "Ring" || item_type == "Earring" {
		return Header{
			buyout:    binary.LittleEndian.Uint32(data[254:]),
			bid:       binary.LittleEndian.Uint32(data[238:]),
			item_type: item_type,
			item_id:   item_id,
		}
	} else {
		return Header{
			buyout:    binary.LittleEndian.Uint32(data[283:]),
			bid:       binary.LittleEndian.Uint32(data[267:]),
			item_type: item_type,
			item_id:   item_id,
		}
	}
}

func ParseData(data []byte) {
	search := data[16:]
	maxResultsPerPage := 10

	currentOffset := 0

	for i := 0; i < maxResultsPerPage; i++ {

		if len(search[currentOffset:]) < item_header_size {
			break
		}

		item_header := getHeader(search[currentOffset:])

		// // break
		if item_header.item_type == "Ring" || item_header.item_type == "Earring" {
			itemStatus := GetEarringRing(search[currentOffset:])

			println(item_header.item_type, itemStatus.stat1, itemStatus.stat2, itemStatus.eng1, itemStatus.eng2, itemStatus.neg, itemStatus.bid, itemStatus.buyout)

			currentOffset += item_header_size + earring_ring_footer_size
		} else {
			itemStatus := GetNecklace(search[currentOffset:])

			println(itemStatus.stat1, itemStatus.stat2, itemStatus.eng1, itemStatus.eng2, itemStatus.neg, itemStatus.bid, itemStatus.buyout)

			currentOffset += item_header_size + necklace_footer_size
		}

	}

}
