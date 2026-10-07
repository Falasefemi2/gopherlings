// 075: context.Context carries cancellation. Parents cancel via
// cancel(); workers watch <-ctx.Done() and stop.
// TODO: stop early when ctx is cancelled.
package main

import (
	"context"
	"time"
)

func Work(ctx context.Context) string {
	time.Sleep(50 * time.Millisecond)
	return "done"
}
