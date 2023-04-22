package market

import (
	"encoding/binary"
	"errors"
	"io/ioutil"
	"os"
	"syscall"
	"unsafe"
)

var (
	state                            []byte
	oodleSharedDict                  []byte
	initDict                         []byte
	workingDir, _                    = os.Getwd()
	oddleDllName                     = "oo2net_9_win64.dll"
	oodleDll                         = syscall.NewLazyDLL(workingDir + "\\" + oddleDllName)
	oodleNetwork1UDP_Decode          = oodleDll.NewProc("OodleNetwork1UDP_Decode")
	oodleNetwork1UDP_State_Uncompact = oodleDll.NewProc("OodleNetwork1UDP_State_Uncompact")
	oodleNetwork1_Shared_SetWindow   = oodleDll.NewProc("OodleNetwork1_Shared_SetWindow")
	oodleNetwork1UDP_State_Size      = oodleDll.NewProc("OodleNetwork1UDP_State_Size")
	oodleNetwork1_Shared_Size        = oodleDll.NewProc("OodleNetwork1_Shared_Size")
)

func OodleNetwork1UDP_Decode(state []byte, shared []byte, comp []byte, compLen int, raw []byte, rawLen int) bool {

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

func OodleNetwork1UDP_State_Uncompact(state []byte, compressorState []byte) bool {
	ret, _, _ := oodleNetwork1UDP_State_Uncompact.Call(
		uintptr(unsafe.Pointer(&state[0])),
		uintptr(unsafe.Pointer(&compressorState[0])),
	)
	return ret != 0
}

func OodleNetwork1_Shared_SetWindow(data []byte, length int, data2 []byte, length2 int) {
	oodleNetwork1_Shared_SetWindow.Call(
		uintptr(unsafe.Pointer(&data[0])),
		uintptr(length),
		uintptr(unsafe.Pointer(&data2[0])),
		uintptr(length2),
	)
}

func OodleNetwork1UDP_State_Size() int {
	ret, _, _ := oodleNetwork1UDP_State_Size.Call()
	return int(ret)
}

func OodleNetwork1_Shared_Size(bits int) int {
	ret, _, _ := oodleNetwork1_Shared_Size.Call(uintptr(bits))
	return int(ret)
}

func Init() {
	oodleState := "oodle_state.bin"
	f, err := ioutil.ReadFile(oodleState)
	if err != nil {
		panic(err)
	}
	initDict = make([]byte, 0x800000)
	copy(initDict, f[0x20:0x20+0x800000])
	compressorSize := binary.LittleEndian.Uint32(f[0x18:])
	compressorState := make([]byte, compressorSize)
	copy(compressorState, f[0x20+0x800000:0x20+0x800000+compressorSize])
	stateSize := OodleNetwork1UDP_State_Size()
	state = make([]byte, stateSize)
	if !OodleNetwork1UDP_State_Uncompact(state, compressorState) {
		panic("oodle init fail")
	}
	oodleSharedDict = make([]byte, OodleNetwork1_Shared_Size(0x13))
	OodleNetwork1_Shared_SetWindow(oodleSharedDict, 0x13, initDict, 0x800000)
}

func Decompress(data []byte) ([]byte, error) {
	outSize := binary.LittleEndian.Uint32(data)

	out_bytes := make([]byte, outSize)

	if !OodleNetwork1UDP_Decode(state, oodleSharedDict, data[4:], len(data)-4, out_bytes, int(outSize)) {
		return nil, errors.New("oodle decompress fail")
	}

	return out_bytes, nil
}
