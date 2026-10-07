package main

import "testing"

func TestDoubleAny(t *testing.T) {
	if DoubleAny(21) != 42 {
		t.Fatal("failed")
	}
}
