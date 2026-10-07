// 051: The comma-ok assertion (x, ok := v.(T)) reports success
// instead of panicking on mismatch. Prefer it at boundaries.
// TODO: return (value, true) for ints, (0, false) otherwise.
package main

func AsInt(v any) (int, bool) {
	return v.(int), true
}
