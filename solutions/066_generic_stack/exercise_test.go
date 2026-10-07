package main

import "testing"

func TestStack(t *testing.T) {
	var s Stack[int]
	s.Push(1)
	s.Push(2)
	if v, _ := s.Pop(); v != 2 {
		t.Fatalf("got %d want 2 (LIFO)", v)
	}
	if v, _ := s.Pop(); v != 1 {
		t.Fatalf("got %d want 1", v)
	}
}
