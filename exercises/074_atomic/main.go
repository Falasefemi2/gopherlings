// 074: sync/atomic gives lock-free counters/flags. Use for a single
// integer; reach for Mutex for compound state. One atomic.AddInt64 is
// a single indivisible step; a separate load plus store is not.
// TODO: increment atomically.
package main

import (
	"sync/atomic"
)

func AtomicTotal(n int) int64 {
	var c int64
	done := make(chan struct{}, n)
	for i := 0; i < n; i++ {
		go func() {
			atomic.AddInt64(&c, 1)
			// tmp := c
			// runtime.Gosched()
			// c = tmp + 1
			done <- struct{}{}
		}()
	}
	for i := 0; i < n; i++ {
		<-done
	}
	return atomic.LoadInt64(&c)
}
