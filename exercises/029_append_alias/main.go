// 029: GOTCHA: slices share backing arrays. append may reuse it,
// so one slice's update can clobber another's. Copy to isolate.
// TODO: make Double return a new slice, leaving the input intact.
package main

func DoubleAll(ns []int) []int {
	out := make([]int, 0, len(ns))
	for _, v := range ns {
		out = append(out, v*2)
	}
	return out
}
