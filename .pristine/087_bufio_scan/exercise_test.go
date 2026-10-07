package main

import "testing"

func TestLines(t *testing.T) {
	if Lines("ab\ncde\nf") != 3 {
		t.Fatalf("got %d", Lines("ab\ncde\nf"))
	}
	if Lines("") != 0 {
		t.Fatal("empty should be 0")
	}
}
