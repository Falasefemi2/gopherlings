// 033: The slices package (Go 1.21+) has Sort, Compact, Clone,
// SortedKeys and friends. Prefer it over hand-rolled loops.
package main

import "slices"

func Sorted(ns []int) []int {
	out := slices.Clone(ns)
	slices.Sort(out)
	return out
}
