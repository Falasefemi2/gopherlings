package main

import "testing"

func TestAtomicTotal(t *testing.T) {
	if AtomicTotal(2000) != 2000 {
		t.Fatalf("got %d", AtomicTotal(2000))
	}
}
