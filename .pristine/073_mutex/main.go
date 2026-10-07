// 073: sync.Mutex serializes access. Lock/Unlock around the shared
// section; run `go test -race` to prove the race is gone.
// A read-modify-write like count++ is three separate steps, and the
// scheduler can slip another goroutine between them (Gosched below
// stands in for real preemption).
// TODO: guard the counter so the total is exact.
package main

import (
	"runtime"
	"sync"
)

func Total(n int) int {
	var wg sync.WaitGroup
	count := 0
	for i := 0; i < n; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			tmp := count
			runtime.Gosched()
			count = tmp + 1
		}()
	}
	wg.Wait()
	return count
}
