// 089: sort.Slice sorts with a less func; slices.Sort handles the
// common ordered case. sort is stable only via sort.SliceStable.
package main

import "sort"

type Human struct {
	Name string
	Age  int
}

func ByAge(h []Human) {
	sort.Slice(h, func(i, j int) bool { return h[i].Age < h[j].Age })
}
