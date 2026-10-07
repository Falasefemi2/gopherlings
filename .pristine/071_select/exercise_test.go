package main

import (
	"testing"
	"time"
)

func TestRace(t *testing.T) {
	fast := make(chan string, 1)
	slow := make(chan string) // never sends: only fast is ready
	fast <- "fast"
	done := make(chan string, 1)
	go func() { done <- Race(fast, slow) }()
	select {
	case got := <-done:
		if got != "fast" {
			t.Fatalf("got %q want fast: slow answered first?", got)
		}
	case <-time.After(500 * time.Millisecond):
		t.Fatal("blocked: nobody answered")
	}
}
