// 076: context.WithTimeout auto-cancels after a deadline. The callee
// sees ctx.Done(); the caller checks ctx.Err() == context.DeadlineExceeded.
// TODO: time out the slow operation.
package main

import (
	"context"
	"time"
)

func Fetch(ctx context.Context) error {
	time.Sleep(200 * time.Millisecond)
	return nil
}
