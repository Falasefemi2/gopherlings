package main

import "testing"

func TestTwoIncs(t *testing.T) {
	if TwoIncs() != 2 {
		t.Fatalf("got %d want 2", TwoIncs())
	}
}
