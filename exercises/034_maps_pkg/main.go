// 034: The maps package (Go 1.21+) has Clone, Equal, Keys, Merge
// style helpers. TODO: return an equal but independent copy.
package main

import "maps"

func Clone(m map[string]int) map[string]int {
	clone := maps.Clone(m)
	return clone
}
