package main

import (
	"testing"
	"time"
)

func TestTwoSends(t *testing.T) {
	done := make(chan int, 1)
	go func() { done <- TwoSends() }()
	select {
	case n := <-done:
		if n != 2 {
			t.Fatalf("got %d want 2", n)
		}
	case <-time.After(500 * time.Millisecond):
		t.Fatal("blocked: unbuffered channel needs a receiver")
	}
}
