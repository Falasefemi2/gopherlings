package main

import "testing"

func TestZero(t *testing.T) {
	n, s, b := Zero()
	if n != 0 || s != "" || b != false {
		t.Fatalf("got (%v,%q,%v), want (0,\"\",false)", n, s, b)
	}
}
