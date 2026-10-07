package main

import "testing"

func TestReverse(t *testing.T) {
	if Reverse("abc") != "cba" {
		t.Fatalf("got %q", Reverse("abc"))
	}
	if Reverse("héllo") != "olléh" {
		t.Fatalf("got %q", Reverse("héllo"))
	}
}
