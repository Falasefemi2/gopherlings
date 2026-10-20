// 078: Fan-in merges many channels into one. Launch one goroutine
// per input, forward until inputs close, then close the output.
// TODO: merge a and b into a single channel.
package main

import "sync"

func FanIn(a, b <-chan int) <-chan int {
	out := make(chan int)
	var wg sync.WaitGroup
	forward := func(ch <-chan int) {
		defer wg.Done()
		for v := range ch {
			out <- v
		}
	}
	wg.Add(2)
	go forward(a)
	go forward(b)
	go func() {
		wg.Wait()
		close(out)
	}()
	return out
}
