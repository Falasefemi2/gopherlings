// 032: Map iteration order is randomized on purpose. For stable
// output, collect keys and sort them (slices.SortedKeys / Sort).
package main

import "sort"

func Keys(m map[string]int) []string {
	out := make([]string, 0, len(m))
	for k := range m {
		out = append(out, k)
	}
	sort.Strings(out)
	return out
}
