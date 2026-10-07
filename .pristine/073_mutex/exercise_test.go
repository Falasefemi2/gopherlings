package main

import "testing"

func TestTotal(t *testing.T) {
	if Total(2000) != 2000 {
		t.Fatalf("got %d want 2000 (lost updates without a mutex?)", Total(2000))
	}
}
