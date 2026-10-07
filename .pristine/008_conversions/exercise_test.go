package main

import "testing"

func TestItoa(t *testing.T) {
	if got := Itoa(65); got != "65" {
		t.Fatalf("got %q, want %q", got, "65")
	}
	if got := Itoa(-7); got != "-7" {
		t.Fatalf("got %q, want %q", got, "-7")
	}
}
