package main

import (
	"errors"
	"testing"
)

func TestBoth(t *testing.T) {
	err := Both()
	if !errors.Is(err, ErrA) || !errors.Is(err, ErrB) {
		t.Fatalf("joined error should match both, got %v", err)
	}
}
