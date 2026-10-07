package main

import "testing"

func TestMin2(t *testing.T) {
	if Min2(2, 1) != 1 {
		t.Fatal("int min failed")
	}
	if Min2("b", "a") != "a" {
		t.Fatal("string min failed")
	}
}
