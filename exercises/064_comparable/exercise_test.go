package main

import "testing"

func TestHas(t *testing.T) {
	if !Has([]string{"a", "b"}, "b") {
		t.Fatal("should find b")
	}
	if Has([]int{1}, 2) {
		t.Fatal("should not find 2")
	}
}
