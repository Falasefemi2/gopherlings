// 050: any is an alias for interface{}. It holds anything; use a
// type assertion (v.(T)) or type switch to get values back.
// TODO: return the underlying int doubled.
package main

func DoubleAny(v any) int {
	s, ok := v.(int)
	if ok {
		return s * 2
	}
	return 0
}
