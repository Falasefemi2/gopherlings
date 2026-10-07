// 034: The maps package (Go 1.21+) has Clone, Equal, Keys, Merge
// style helpers. TODO: return an equal but independent copy.
package main

func Clone(m map[string]int) map[string]int {
	return m
}
