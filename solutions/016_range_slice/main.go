// 016: `for i, v := range s` copies each element into v.
// Assigning to v does not touch the slice; use s[i].
package main

func Double(ns []int) []int {
	for i := range ns {
		ns[i] *= 2
	}
	return ns
}
