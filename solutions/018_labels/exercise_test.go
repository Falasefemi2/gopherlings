package main

import "testing"

func TestFind(t *testing.T) {
	m := [][]int{{1, 2}, {3, 4}}
	r, c, ok := Find(4, m)
	if !ok || r != 1 || c != 1 {
		t.Fatalf("got %d,%d,%v", r, c, ok)
	}
	if _, _, ok := Find(9, m); ok {
		t.Fatal("should not find 9")
	}
}
