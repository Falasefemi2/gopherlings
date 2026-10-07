package main

import "testing"

func TestCall(t *testing.T) {
	if Call() != "hi bob!" {
		t.Fatalf("got %q", Call())
	}
}
