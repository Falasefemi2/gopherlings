// 034: The maps package (Go 1.21+) has Clone, Equal, Keys, Merge
// style helpers.
package main

import "maps"

func Clone(m map[string]int) map[string]int {
	return maps.Clone(m)
}
