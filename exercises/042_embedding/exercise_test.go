package main

import "testing"

func TestEmbed(t *testing.T) {
	s := NewServer()
	if s.Log("hi") != "log:hi" {
		t.Fatal("promoted Log failed (nil embedded Logger?)")
	}
}
