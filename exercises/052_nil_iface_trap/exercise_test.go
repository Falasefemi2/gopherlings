package main

import "testing"

func TestCheck(t *testing.T) {
	if err := Check(true); err != nil {
		t.Fatalf("success should be nil error, got %#v", err)
	}
	if err := Check(false); err == nil {
		t.Fatal("failure should be non-nil")
	}
}
