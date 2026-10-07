package main

import "testing"

func TestAtomicTotal(t *testing.T) {
	if got := AtomicTotal(2000); got != 2000 {
		t.Fatalf("got %d want 2000", got)
	}
}
