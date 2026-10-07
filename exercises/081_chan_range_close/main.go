// 081: GOTCHA: `for v := range ch` ends only when ch is closed.
// The sender closes when done; receivers must not double-close.
// TODO: close the channel after sending.
package main

func Sum3() int {
	ch := make(chan int)
	go func() {
		ch <- 1
		ch <- 2
		ch <- 3
	}()
	sum := 0
	for v := range ch {
		sum += v
	}
	return sum
}
