package main

import "testing"

func TestRead3(t *testing.T) {
	s, err := Read3(Three{})
	if err != nil || s != "abc" {
		t.Fatalf("got %q,%v", s, err)
	}
}
