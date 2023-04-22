package main

import (
	"encoding/binary"
	"os"
	"syscall"
	"unsafe"
)

func test() {
	oodleState := "oodle_state.bin"

	f, err := os.Open(oodleState)

	if err != nil {
		panic(err)
	}
	
	defer f.Close()

	// -----------
	var sharedBits, compactSharedSize int32

	f.Seek(0x08, 0)
	binary.Read(f, binary.LittleEndian, &sharedBits)
	binary.Read(f, binary.LittleEndian, &compactSharedSize)

	// -----------
	f.Seek(0x18, 0)
	var compactStateSize int32

	binary.Read(f, binary.LittleEndian, &compactStateSize)

	// compactedShared := make([]byte, compactSharedSize)
	// compactedSharedRef := (*uint8)(unsafe.Pointer(&compactedShared[0]))

	compactedState := make([]byte, compactStateSize)
	f.Read(compactedState)

	oddleDllHandle := syscall.MustLoadDLL("D:/projects/market-parser/meter-data/oo2net_9_win64.dll")

	if err != nil {
		panic(err)
	}


	oodleStateSizeProc := oddleDllHandle.MustFindProc("OodleNetwork1UDP_State_Size")
	
	if err != nil {
		panic(err)
	}

	stateSize, _, _ := oodleStateSizeProc.Call()

	state := make([]byte, stateSize)

	oddleStateUncompactProc := oddleDllHandle.MustFindProc("OodleNetwork1UDP_State_Uncompact")


	ret, _, _ := oddleStateUncompactProc.Call(
		uintptr(unsafe.Pointer(&state)), 
		uintptr(unsafe.Pointer(&compactedState)),
	)

	println(ret)

	oddleSharedSize := oddleDllHandle.MustFindProc("OodleNetwork1_Shared_Size")

	shared, _, _ := oddleSharedSize.Call(
		uintptr(sharedBits),
	)

	// oddleSharedSetWindow := oddleDllHandle.MustFindProc("OodleNetwork1_Shared_SetWindow")

	// oddleSharedSetWindow.Call(
	// 	uintptr(unsafe.Pointer(&shared)),
	// 	uintptr(sharedBits),
	// 	uintptr(unsafe.Pointer(&compactedShared)),
	// 	uintptr(compactSharedSize),
	// )

	oddle_decode := oddleDllHandle.MustFindProc("OodleNetwork1UDP_Decode")



	data := make([]byte, 12)
	outSize := binary.BigEndian.Uint32(data[0:4])

	payload := make([]byte, outSize-4)
	out := make([]byte, outSize)

	print(out)


	oddle_decode.Call(
		uintptr(unsafe.Pointer(&state)),
		uintptr(unsafe.Pointer(&shared)),
		uintptr(unsafe.Pointer(&payload)),
		uintptr(len(data) - 4),
		uintptr(unsafe.Pointer(&out)),
		uintptr(outSize),
	)


	print(out)




}