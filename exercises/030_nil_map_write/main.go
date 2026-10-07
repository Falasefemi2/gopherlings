// 030: GOTCHA: a nil map reads fine but writing panics.
// Declare with make or a literal before inserting.
// TODO: stop the panic when inserting.
package main

func Put(m map[string]int, k string, v int) map[string]int {
	m[k] = v
	return m
}
