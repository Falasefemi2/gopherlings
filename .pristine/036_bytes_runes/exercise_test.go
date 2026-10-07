package main

import "testing"

func TestRuneLen(t *testing.T) {
	if RuneLen("héllo") != 5 {
		t.Fatalf("got %d want 5", RuneLen("héllo"))
	}
	if RuneLen("go") != 2 {
		t.Fatal("ascii failed")
	}
}
