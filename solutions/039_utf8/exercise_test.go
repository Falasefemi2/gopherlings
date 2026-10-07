package main

import "testing"

func TestFirstRune(t *testing.T) {
	if FirstRune("éclair") != 'é' {
		t.Fatalf("got %q", FirstRune("éclair"))
	}
}
