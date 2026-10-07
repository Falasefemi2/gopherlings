// 090: Table-driven tests loop over (input, want) rows, often with
// subtests via t.Run. One func covers the whole matrix.
// TODO: fix Abs so every row passes.
package main

func Abs(n int) int {
	if n < 0 {
		return n
	}
	return n
}
