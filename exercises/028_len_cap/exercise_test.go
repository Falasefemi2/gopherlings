package main

import "testing"

func TestLenCap(t *testing.T) {
	l, c := LenCap()
	if l != 2 || c != 5 {
		t.Fatalf("got len=%d cap=%d", l, c)
	}
}
