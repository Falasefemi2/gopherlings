package main

import "testing"

func TestScaled(t *testing.T) {
	if got := Scaled(); got.W != 20 || got.H != 30 {
		t.Fatalf("got %+v", got)
	}
}
