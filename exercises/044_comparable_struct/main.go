// 044: Structs with only comparable fields support == and can be
// map keys. A slice/map field makes == a compile error.
// TODO: keep the struct comparable and the equality true.
package main

import "reflect"

type Key struct {
	A string
	B []int
}

func Same() bool {
	a := Key{A: "x", B: []int{1}}
	b := Key{A: "x", B: []int{1}}
	return reflect.DeepEqual(a, b)
}
