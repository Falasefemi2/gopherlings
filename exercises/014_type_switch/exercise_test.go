package main

import "testing"

func TestDescribe(t *testing.T) {
	if Describe("hi") != "str:hi" {
		t.Fatalf("got %q", Describe("hi"))
	}
	if Describe(42) != "int:42" {
		t.Fatalf("got %q", Describe(42))
	}
}
