package main

import "testing"

func TestSet(t *testing.T) {
	n := 0
	Set(&n)
	if n != 99 {
		t.Fatalf("got %d", n)
	}
}
