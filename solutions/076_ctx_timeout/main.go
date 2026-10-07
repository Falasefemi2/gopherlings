// 076: context.WithTimeout auto-cancels after a deadline. The callee
// sees ctx.Done(); the caller checks ctx.Err() == context.DeadlineExceeded.
package main

import (
	"context"
	"time"
)

func Fetch(ctx context.Context) error {
	select {
	case <-time.After(200 * time.Millisecond):
		return nil
	case <-ctx.Done():
		return ctx.Err()
	}
}
