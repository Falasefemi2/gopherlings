// 020: GOTCHA: defer inside a loop waits until the FUNCTION returns,
// not the iteration. For files/locks in loops, close explicitly.
// TODO: keep at most 1 slot open at a time.
package main

func MaxOpen(n int) int {
	open, max := 0, 0
	for i := 0; i < n; i++ {
		open++
		if open > max {
			max = open
		}
		open--
	}
	return max
}
