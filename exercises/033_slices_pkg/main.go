// 033: The slices package (Go 1.21+) has Sort, Compact, Clone,
// SortedKeys and friends. Prefer it over hand-rolled loops.
// TODO: return the sorted copy.
package main

import "sort"

func Sorted(ns []int) []int {
	sort.Ints(ns)
	return ns
}
