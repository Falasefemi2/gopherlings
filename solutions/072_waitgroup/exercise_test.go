package main

import "testing"

func TestCount10(t *testing.T) {
	for i := 0; i < 20; i++ {
		if Count10() != 10 {
			t.Fatalf("got %d want 10", Count10())
		}
	}
}
