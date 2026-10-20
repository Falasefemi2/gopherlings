// 080: errgroup pattern by hand: one goroutine per task, a buffered
// error channel (or mutex), Wait for all, return the first error.
// TODO: return the first non-nil error (if any).
package main

import (
	"context"

	"golang.org/x/sync/errgroup"
)

func RunAll(fs []func() error) error {
	g, _ := errgroup.WithContext(context.Background())

	for _, f := range fs {
		f := f // capture this iteration's function
		g.Go(func() error {
			return f()
		})
	}

	return g.Wait()
}
