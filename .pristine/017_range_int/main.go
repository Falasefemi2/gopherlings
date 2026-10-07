// 017: Since Go 1.22 you can range directly over an integer:
// `for i := range n` yields 0..n-1 (n values total).
// TODO: return exactly n values: 0..n-1.
package main

func First(n int) []int {
	var out []int
	for i := 0; i <= n; i++ {
		out = append(out, i)
	}
	return out
}
