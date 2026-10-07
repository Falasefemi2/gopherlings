package main

import "testing"

func TestTotal(t *testing.T) {
	if got := Total(2000); got != 2000 {
		t.Fatalf("got %d want 2000 (lost updates without a mutex?)", got)
	}
}
