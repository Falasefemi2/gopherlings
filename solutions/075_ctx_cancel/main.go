// 075: context.Context carries cancellation. Parents cancel via
// cancel(); workers watch <-ctx.Done() and stop.
package main

import (
	"context"
	"time"
)

func Work(ctx context.Context) string {
	select {
	case <-time.After(50 * time.Millisecond):
		return "done"
	case <-ctx.Done():
		return "cancelled:" + ctx.Err().Error()
	}
}
