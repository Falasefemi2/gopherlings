// 080: errgroup pattern by hand: one goroutine per task, a buffered
// error channel (or mutex), Wait for all, return the first error.
package main

import "sync"

func RunAll(fs []func() error) error {
	var wg sync.WaitGroup
	errs := make(chan error, len(fs))
	for _, f := range fs {
		wg.Add(1)
		go func() {
			defer wg.Done()
			if err := f(); err != nil {
				errs <- err
			}
		}()
	}
	wg.Wait()
	close(errs)
	for err := range errs {
		return err
	}
	return nil
}
