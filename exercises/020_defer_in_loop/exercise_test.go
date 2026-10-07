package main

import "testing"

func TestMaxOpen(t *testing.T) {
	if got := MaxOpen(5); got != 1 {
		t.Fatalf("got maxOpen=%d want 1", got)
	}
}
