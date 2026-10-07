package main

import "testing"

func TestApply(t *testing.T) {
	double := func(n int) int { return 2 * n }
	if Apply(double, 3) != 6 {
		t.Fatal("Apply should call f")
	}
}
