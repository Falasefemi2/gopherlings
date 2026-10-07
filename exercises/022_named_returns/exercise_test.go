package main

import "testing"

func TestSwap(t *testing.T) {
	x, y := Swap(1, 2)
	if x != 2 || y != 1 {
		t.Fatalf("got %d,%d", x, y)
	}
}
