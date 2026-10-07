// 024: Closures capture surrounding variables by reference.
// Each call to Counter must keep its own state.
// TODO: return a func counting 1,2,3... per call.
package main

func Counter() func() int {
	sum := 0
	return func() int {
		sum++
		return sum
	}
}
