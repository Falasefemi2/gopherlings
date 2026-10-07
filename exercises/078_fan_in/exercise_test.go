package main

import (
	"sort"
	"testing"
)

func TestFanIn(t *testing.T) {
	a := make(chan int, 2)
	b := make(chan int, 2)
	a <- 1
	a <- 3
	close(a)
	b <- 2
	close(b)
	var got []int
	for v := range FanIn(a, b) {
		got = append(got, v)
	}
	sort.Ints(got)
	if len(got) != 3 || got[0] != 1 || got[1] != 2 || got[2] != 3 {
		t.Fatalf("got %v", got)
	}
}
