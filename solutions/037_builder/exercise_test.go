package main

import "testing"

func TestJoin(t *testing.T) {
	if Join([]string{"a", "b", "c"}) != "abc" {
		t.Fatalf("got %q", Join([]string{"a", "b", "c"}))
	}
	if Join(nil) != "" {
		t.Fatal("nil should join to empty")
	}
}
