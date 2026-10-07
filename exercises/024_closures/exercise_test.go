package main

import "testing"

func TestCounter(t *testing.T) {
	c := Counter()
	for want := 1; want <= 3; want++ {
		if got := c(); got != want {
			t.Fatalf("got %d want %d", got, want)
		}
	}
}
