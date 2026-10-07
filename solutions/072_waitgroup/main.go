// 072: sync.WaitGroup waits for a set of goroutines. Add before
// starting them, Done when each ends (often deferred), Wait at the end.
package main

import "sync"

func Count10() int {
	var mu sync.Mutex
	n := 0
	var wg sync.WaitGroup
	for i := 0; i < 10; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			mu.Lock()
			n++
			mu.Unlock()
		}()
	}
	wg.Wait()
	return n
}
