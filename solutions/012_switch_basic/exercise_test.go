package main

import "testing"

func TestDay(t *testing.T) {
	if Day(1) != "Mon" {
		t.Fatalf("got %q want Mon", Day(1))
	}
	if Day(2) != "Tue" {
		t.Fatalf("got %q want Tue", Day(2))
	}
	if Day(9) != "?" {
		t.Fatalf("got %q want ?", Day(9))
	}
}
