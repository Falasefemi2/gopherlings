// 078: Fan-in merges many channels into one. Launch one goroutine
// per input, forward until inputs close, then close the output.
// TODO: merge a and b into a single channel.
package main

func FanIn(a, b <-chan int) <-chan int {
	out := make(chan int)
	go func() {
		for v := range a {
			out <- v
		}
		close(out)
	}()
	return out
}
