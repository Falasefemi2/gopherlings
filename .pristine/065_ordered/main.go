// 065: cmp.Ordered covers ints, floats and strings for <,>.
// Import "cmp"; constraints live in signatures, not bodies.
// TODO: return the smaller of a and b.
package main

func Min2[T cmp.Ordered](a, b T) T {
	if a < b {
		return a
	}
	return b
}
