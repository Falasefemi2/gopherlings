package main

import "testing"

func TestFail(t *testing.T) {
	if Fail(false) != nil {
		t.Fatal("success should be nil")
	}
	if Fail(true) == nil {
		t.Fatal("failure should be non-nil")
	}
}
