// 073: sync.Mutex serializes access. Lock/Unlock around the shared
// section; run `go test -race` to prove the race is gone.
package main

import "sync"

func Total(n int) int {
	var wg sync.WaitGroup
	var mu sync.Mutex
	count := 0
	for i := 0; i < n; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			mu.Lock()
			count++
			mu.Unlock()
		}()
	}
	wg.Wait()
	return count
}
