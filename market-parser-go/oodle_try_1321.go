package main

import (
	"os"
	"syscall"
	"unsafe"
)

type Oodle struct{}

var (
	oodleDll = syscall.NewLazyDLL("oo2net_9_win64")

	oodleNetwork1UDP_Decode          = oodleDll.NewProc("OodleNetwork1UDP_Decode")
	oodleNetwork1UDP_State_Uncompact = oodleDll.NewProc("OodleNetwork1UDP_State_Uncompact")
	oodleNetwork1_Shared_SetWindow   = oodleDll.NewProc("OodleNetwork1_Shared_SetWindow")
	oodleNetwork1UDP_State_Size      = oodleDll.NewProc("OodleNetwork1UDP_State_Size")
	oodleNetwork1_Shared_Size        = oodleDll.NewProc("OodleNetwork1_Shared_Size")
)

func (o *Oodle) OodleNetwork1UDP_Decode(state []byte, shared []byte, comp []byte, compLen int, raw []byte, rawLen int) bool {
	ret, _, _ := oodleNetwork1UDP_Decode.Call(
		uintptr(unsafe.Pointer(&state[0])),
		uintptr(unsafe.Pointer(&shared[0])),
		uintptr(unsafe.Pointer(&comp[0])),
		uintptr(compLen),
		uintptr(unsafe.Pointer(&raw[0])),
		uintptr(rawLen),
	)
	return ret != 0
}

func (o *Oodle) OodleNetwork1UDP_State_Uncompact(state []byte, compressorState []byte) bool {
	ret, _, _ := oodleNetwork1UDP_State_Uncompact.Call(
		uintptr(unsafe.Pointer(&state[0])),
		uintptr(unsafe.Pointer(&compressorState[0])),
	)
	return ret != 0
}

func (o *Oodle) OodleNetwork1_Shared_SetWindow(data []byte, length int, data2 []byte, length2 int) {
	oodleNetwork1_Shared_SetWindow.Call(
		uintptr(unsafe.Pointer(&data[0])),
		uintptr(length),
		uintptr(unsafe.Pointer(&data2[0])),
		uintptr(length2),
	)
}

func (o *Oodle) OodleNetwork1UDP_State_Size() int {
	ret, _, _ := oodleNetwork1UDP_State_Size.Call()
	return int(ret)
}

func (o *Oodle) OodleNetwork1_Shared_Size(bits int) int {
	ret, _, _ := oodleNetwork1_Shared_Size.Call(uintptr(bits))
	return int(ret)
}

func init() {
	oodleState := "oodle_state.bin"

	f, err := os.Open(oodleState)

	if err != nil {
		panic(err)
	}
	defer f.Close()

	println(f)
}
