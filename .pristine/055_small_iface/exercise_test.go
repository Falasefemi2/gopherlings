package main

import (
	"bytes"
	"testing"
)

func TestWrite3(t *testing.T) {
	var b bytes.Buffer
	n, err := Write3(&b)
	if err != nil || n != 3 || b.String() != "hey" {
		t.Fatalf("got %d %q %v", n, b.String(), err)
	}
}
