// 005: const values are fixed at compile time. iota counts
// 0,1,2... per line inside a const block. Great for enums.
// TODO: use iota so A=0, B=1, C=2.
package main

const (
	A = iota
	B
	C
)
