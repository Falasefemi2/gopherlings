package main

import "testing"

func TestByAge(t *testing.T) {
	h := []Human{{"c", 30}, {"a", 20}, {"b", 25}}
	ByAge(h)
	if h[0].Age != 20 || h[1].Age != 25 || h[2].Age != 30 {
		t.Fatalf("got %+v", h)
	}
}
