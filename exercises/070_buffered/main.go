// 070: Unbuffered sends block until a receiver arrives. Buffered
// sends (make(chan T, n)) block only when the buffer is full.
// TODO: make the two sends succeed with no receiver yet.
package main

func TwoSends() int {
	ch := make(chan int)
	ch <- 1
	ch <- 2
	return len(ch)
}
