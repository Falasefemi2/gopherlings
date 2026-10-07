package main

import "testing"

func TestRace(t *testing.T) {
	fast := make(chan string, 1)
	slow := make(chan string, 1)
	fast <- "fast"
	slow <- "slow"
	if Race(fast, slow) != "fast" {
		t.Fatal("fast channel should win")
	}
}
