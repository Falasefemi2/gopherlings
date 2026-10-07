// 005: const values are fixed at compile time. iota counts
// 0,1,2... per line inside a const block. Great for enums.
package main

const (
	A = iota
	B
	C
)
