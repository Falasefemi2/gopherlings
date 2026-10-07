package main

import "testing"

func TestDecode(t *testing.T) {
	r, err := Decode(`{"temp":21.5,"unit":"C"}`)
	if err != nil || r.Temp != 21.5 || r.Unit != "C" {
		t.Fatalf("got %+v,%v", r, err)
	}
	if _, err := Decode(`{bad}`); err == nil {
		t.Fatal("expected error for bad JSON")
	}
}
