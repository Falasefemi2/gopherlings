package main

import (
	"errors"
	"testing"
)

func TestWrap(t *testing.T) {
	if !errors.Is(Middle(), ErrBase) {
		t.Fatalf("chain broken: %v", Middle())
	}
}
