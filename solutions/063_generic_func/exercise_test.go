package main

import "testing"

func TestFirst2(t *testing.T) {
	if First2([]int{7, 8}) != 7 {
		t.Fatal("int failed")
	}
	if First2([]string{"a"}) != "a" {
		t.Fatal("string failed")
	}
	if First2[int](nil) != 0 {
		t.Fatal("empty should be zero")
	}
}
