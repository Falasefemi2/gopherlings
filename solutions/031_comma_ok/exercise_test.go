package main

import "testing"

func TestLookup(t *testing.T) {
	m := map[string]int{"a": 0}
	if _, ok := Lookup(m, "missing"); ok {
		t.Fatal("missing key should report ok=false")
	}
	if v, ok := Lookup(m, "a"); !ok || v != 0 {
		t.Fatalf("got %d,%v", v, ok)
	}
}
