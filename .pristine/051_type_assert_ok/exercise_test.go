package main

import "testing"

func TestAsInt(t *testing.T) {
	if n, ok := AsInt(5); !ok || n != 5 {
		t.Fatal("int failed")
	}
	if _, ok := AsInt("x"); ok {
		t.Fatal("string should not assert")
	}
}
