package main

import "testing"

func TestStringer(t *testing.T) {
	if Greet2(Person{Name: "ann"}) != "user:ann" {
		t.Fatalf("got %q", Greet2(Person{Name: "ann"}))
	}
}
