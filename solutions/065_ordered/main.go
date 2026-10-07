// 065: cmp.Ordered covers ints, floats and strings for <,>.
// Import "cmp"; constraints live in signatures, not bodies.
package main

import "cmp"

func Min2[T cmp.Ordered](a, b T) T {
	if a < b {
		return a
	}
	return b
}
