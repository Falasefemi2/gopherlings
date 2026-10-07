package main

import "testing"

func TestPutNil(t *testing.T) {
	defer func() {
		if r := recover(); r != nil {
			t.Fatalf("panicked on nil map write: %v", r)
		}
	}()
	m := Put(nil, "a", 1)
	if m["a"] != 1 {
		t.Fatalf("got %v", m)
	}
}
