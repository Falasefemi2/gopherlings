package main

import "testing"

func TestIota(t *testing.T) {
	if A != 0 || B != 1 || C != 2 {
		t.Fatalf("got A=%d B=%d C=%d, want 0 1 2", A, B, C)
	}
}
