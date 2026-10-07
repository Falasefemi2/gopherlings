package main

import "testing"

func TestTags(t *testing.T) {
	if got := ToJSON(); got != `{"name":"ann","age":3}` {
		t.Fatalf("got %s", got)
	}
}
