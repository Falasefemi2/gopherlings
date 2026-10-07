package main

import "testing"

func TestLRU(t *testing.T) {
	c := NewLRU(2)
	c.Put("a", 1)
	c.Put("b", 2)
	if v, ok := c.Get("a"); !ok || v != 1 {
		t.Fatalf("get a: %v %v", v, ok)
	}
	c.Put("c", 3) // evicts b (a was just used)
	if _, ok := c.Get("b"); ok {
		t.Fatal("b should have been evicted")
	}
	if v, ok := c.Get("c"); !ok || v != 3 {
		t.Fatalf("get c: %v %v", v, ok)
	}
	c.Put("a", 10)
	if v, ok := c.Get("a"); !ok || v != 10 {
		t.Fatalf("update a: %v %v", v, ok)
	}
}
