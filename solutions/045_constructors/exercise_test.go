package main

import "testing"

func TestAccount(t *testing.T) {
	if _, err := NewAccount(""); err == nil {
		t.Fatal("expected error for empty name")
	}
	a, err := NewAccount("ann")
	if err != nil || a.Name != "ann" {
		t.Fatalf("got %+v,%v", a, err)
	}
}
