package main

import "testing"

func TestSumTo(t *testing.T) {
	if SumTo(5) != 15 {
		t.Fatalf("got %d want 15", SumTo(5))
	}
	if SumTo(1) != 1 {
		t.Fatalf("got %d want 1", SumTo(1))
	}
}
