package main

import "testing"

func TestSum(t *testing.T) {
	if Sum(1, 2, 3) != 6 {
		t.Fatalf("got %d", Sum(1, 2, 3))
	}
	if Sum() != 0 {
		t.Fatal("empty sum should be 0")
	}
	s := []int{4, 5}
	if Sum(s...) != 9 {
		t.Fatal("spread call failed")
	}
}
