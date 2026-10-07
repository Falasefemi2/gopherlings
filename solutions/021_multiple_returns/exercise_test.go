package main

import "testing"

func TestSplit(t *testing.T) {
	h, p := SplitHostPort("localhost:8080")
	if h != "localhost" || p != "8080" {
		t.Fatalf("got %q,%q", h, p)
	}
}
