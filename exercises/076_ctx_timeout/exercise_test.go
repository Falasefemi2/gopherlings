package main

import (
	"context"
	"testing"
	"time"
)

func TestFetchTimeout(t *testing.T) {
	ctx, cancel := context.WithTimeout(context.Background(), 20*time.Millisecond)
	defer cancel()
	if err := Fetch(ctx); err != context.DeadlineExceeded {
		t.Fatalf("got %v", err)
	}
}
