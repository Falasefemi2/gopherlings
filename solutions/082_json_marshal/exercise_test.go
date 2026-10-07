package main

import "testing"

func TestEncode(t *testing.T) {
	if got := Encode(); got != `{"name":"ann","age":3}` {
		t.Fatalf("got %s", got)
	}
}
