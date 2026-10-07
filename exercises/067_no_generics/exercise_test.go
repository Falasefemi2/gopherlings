package main

import "testing"

func TestDescribeAny(t *testing.T) {
	if DescribeAny(42) != "42 (int)" {
		t.Fatalf("got %q", DescribeAny(42))
	}
}
