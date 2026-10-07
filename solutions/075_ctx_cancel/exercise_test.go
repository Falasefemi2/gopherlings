package main

import (
	"context"
	"strings"
	"testing"
	"time"
)

func TestWork(t *testing.T) {
	ctx, cancel := context.WithCancel(context.Background())
	cancel()
	if got := Work(ctx); !strings.HasPrefix(got, "cancelled") {
		t.Fatalf("got %q", got)
	}
	if got := Work(context.Background()); got != "done" {
		t.Fatalf("got %q", got)
	}
	_ = time.Now
}
