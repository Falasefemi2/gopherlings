// 078: Fan-in merges many channels into one. Launch one goroutine
// per input, forward until inputs close, then close the output.
package main

import "sync"

func FanIn(a, b <-chan int) <-chan int {
	out := make(chan int)
	var wg sync.WaitGroup
	wg.Add(2)
	go func() {
		defer wg.Done()
		for v := range a {
			out <- v
		}
	}()
	go func() {
		defer wg.Done()
		for v := range b {
			out <- v
		}
	}()
	go func() { wg.Wait(); close(out) }()
	return out
}
