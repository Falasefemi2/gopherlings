package main

import "testing"

func TestLetter(t *testing.T) {
	cases := map[int]string{95: "A", 85: "B", 75: "C", 10: "F"}
	for in, want := range cases {
		if got := Letter(in); got != want {
			t.Fatalf("Letter(%d)=%q want %q", in, got, want)
		}
	}
}
