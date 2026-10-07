// 015: for is the only loop. `for i := 1; i <= n; i++` sums 1..n.
// TODO: include n in the sum.
package main

func SumTo(n int) int {
	sum := 0
	for i := 1; i < n; i++ {
		sum += i
	}
	return sum
}
