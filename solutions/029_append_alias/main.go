// 029: GOTCHA: slices share backing arrays. append may reuse it,
// so one slice's update can clobber another's. Copy to isolate.
package main

func DoubleAll(ns []int) []int {
	out := make([]int, len(ns))
	for i, v := range ns {
		out[i] = v * 2
	}
	return out
}
