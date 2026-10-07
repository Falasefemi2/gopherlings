// 020: GOTCHA: defer inside a loop waits until the FUNCTION returns,
// not the iteration. For files/locks in loops, close explicitly.
package main

func MaxOpen(n int) int {
	open, max := 0, 0
	for i := 0; i < n; i++ {
		open++
		if open > max {
			max = open
		}
		open-- // close/end of iteration: do not defer in a loop
	}
	return max
}
