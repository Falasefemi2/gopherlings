package main

import "testing"

func TestP(t *testing.T) {
	p := P()
	if p.X != 1 || p.Y != 2 {
		t.Fatalf("got %+v", p)
	}
}
