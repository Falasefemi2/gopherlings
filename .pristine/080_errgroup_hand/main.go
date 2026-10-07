// 080: errgroup pattern by hand: one goroutine per task, a buffered
// error channel (or mutex), Wait for all, return the first error.
// TODO: return the first non-nil error (if any).
package main

import "sync"

func RunAll(fs []func() error) error {
	var wg sync.WaitGroup
	for _, f := range fs {
		wg.Add(1)
		go func() {
			defer wg.Done()
			_ = f()
		}()
	}
	wg.Wait()
	return nil
}
