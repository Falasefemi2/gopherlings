// 050: any is an alias for interface{}. It holds anything; use a
// type assertion (v.(T)) or type switch to get values back.
package main

func DoubleAny(v any) int {
	return v.(int) * 2
}
