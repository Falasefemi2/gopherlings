// 073: sync.Mutex serializes access. Lock/Unlock around the shared
// section; run `go test -race` to prove the race is gone.
// TODO: guard the counter so the total is exact.
package main

import "sync"

func Total(n int) int {
	var wg sync.WaitGroup
	count := 0
	for i := 0; i < n; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			count++
		}()
	}
	wg.Wait()
	return count
}
