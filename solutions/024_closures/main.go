// 024: Closures capture surrounding variables by reference.
// Each call to Counter must keep its own state.
package main

func Counter() func() int {
	n := 0
	return func() int {
		n++
		return n
	}
}
