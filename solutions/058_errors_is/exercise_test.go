package main

import "testing"

func TestIsGone(t *testing.T) {
	if !IsGone(Gone()) {
		t.Fatal("should detect wrapped ErrGone")
	}
	if IsGone(nil) {
		t.Fatal("nil is not gone")
	}
}
