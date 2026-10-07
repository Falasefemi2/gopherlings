package main

import (
	"maps"
	"testing"
)

func TestClone(t *testing.T) {
	src := map[string]int{"a": 1}
	got := Clone(src)
	if !maps.Equal(got, src) {
		t.Fatalf("got %v", got)
	}
	got["a"] = 99
	if src["a"] != 1 {
		t.Fatal("clone shares storage with source")
	}
}
