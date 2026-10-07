package main

import (
	"testing"
	"time"
)

func TestSum3(t *testing.T) {
	done := make(chan int, 1)
	go func() { done <- Sum3() }()
	select {
	case n := <-done:
		if n != 6 {
			t.Fatalf("got %d", n)
		}
	case <-time.After(500 * time.Millisecond):
		t.Fatal("deadlock: range never ends without close")
	}
}
