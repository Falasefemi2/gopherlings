// 072: sync.WaitGroup waits for a set of goroutines. Add before
// starting them, Done when each ends (often deferred), Wait at the end.
// TODO: wait for all 10 increments.
package main

import "sync"

func Count10() int {
	var wg sync.WaitGroup
	n := 0

	wg.Go(func() {
		for i := 0; i < 10; i++ {
			n++
		}
	})

	wg.Wait()
	return n
}
