// 044: Structs with only comparable fields support == and can be
// map keys. A slice/map field makes == a compile error.
package main

type Key struct {
	A string
	B int
}

func Same() bool {
	return Key{A: "x", B: 1} == Key{A: "x", B: 1}
}
