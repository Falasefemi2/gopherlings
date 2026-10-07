package main

import (
	"errors"
	"testing"
)

func TestRunAll(t *testing.T) {
	ok := func() error { return nil }
	bad := func() error { return errors.New("x") }
	if err := RunAll([]func() error{ok, ok}); err != nil {
		t.Fatalf("got %v", err)
	}
	if err := RunAll([]func() error{ok, bad}); err == nil {
		t.Fatal("expected error")
	}
}
