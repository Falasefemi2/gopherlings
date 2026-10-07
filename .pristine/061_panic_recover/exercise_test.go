package main

import "testing"

func TestSafe(t *testing.T) {
	if err := Safe(Boom2); err == nil {
		t.Fatal("expected panic converted to error")
	}
	if err := Safe(func() {}); err != nil {
		t.Fatalf("no panic should be nil, got %v", err)
	}
}
