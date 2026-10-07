package main

import "testing"

func TestParseAge(t *testing.T) {
	if n, err := ParseAge("42"); err != nil || n != 42 {
		t.Fatalf("got %d,%v", n, err)
	}
	if _, err := ParseAge("abc"); err == nil {
		t.Fatal("expected error for abc")
	}
}
