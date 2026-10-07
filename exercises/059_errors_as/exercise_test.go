package main

import "testing"

func TestFieldOf(t *testing.T) {
	if FieldOf(Bad()) != "age" {
		t.Fatalf("got %q", FieldOf(Bad()))
	}
	if FieldOf(nil) != "" {
		t.Fatal("nil has no field")
	}
}
