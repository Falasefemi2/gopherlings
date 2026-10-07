package main

import (
	"errors"
	"testing"
)

func TestClassify(t *testing.T) {
	if !errors.Is(Classify(""), ErrMissing) {
		t.Fatal("empty should be ErrMissing")
	}
	var bv *BadValue
	if !errors.As(Classify("zzz"), &bv) {
		t.Fatal("other should be *BadValue")
	}
}
