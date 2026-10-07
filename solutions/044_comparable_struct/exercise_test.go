package main

import "testing"

func TestSame(t *testing.T) {
	if !Same() {
		t.Fatal("expected structs to be equal")
	}
}
