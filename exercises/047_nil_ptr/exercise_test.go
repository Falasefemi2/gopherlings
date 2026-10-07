package main

import "testing"

func TestDeref(t *testing.T) {
	if Deref(nil) != 0 {
		t.Fatal("nil should give 0")
	}
	n := 7
	if Deref(&n) != 7 {
		t.Fatal("non-nil failed")
	}
}
