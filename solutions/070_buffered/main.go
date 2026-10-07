// 070: Unbuffered sends block until a receiver arrives. Buffered
// sends (make(chan T, n)) block only when the buffer is full.
package main

func TwoSends() int {
	ch := make(chan int, 2)
	ch <- 1
	ch <- 2
	return len(ch)
}
