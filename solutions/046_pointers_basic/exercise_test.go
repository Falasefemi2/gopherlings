package main

import "testing"

func TestInc(t *testing.T) {
	n := 1
	Inc(&n)
	if n != 2 {
		t.Fatalf("got %d", n)
	}
}
