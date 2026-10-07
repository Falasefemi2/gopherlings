// 017: Since Go 1.22 you can range directly over an integer:
// `for i := range n` yields 0..n-1 (n values total).
package main

func First(n int) []int {
	var out []int
	for i := range n {
		out = append(out, i)
	}
	return out
}
