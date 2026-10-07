// 051: The comma-ok assertion (x, ok := v.(T)) reports success
// instead of panicking on mismatch. Prefer it at boundaries.
package main

func AsInt(v any) (int, bool) {
	n, ok := v.(int)
	return n, ok
}
