package main

import "testing"

func TestSumAsync(t *testing.T) {
	if SumAsync([]int{1, 2, 3, 4}) != 10 {
		t.Fatalf("got %d", SumAsync([]int{1, 2, 3, 4}))
	}
}
