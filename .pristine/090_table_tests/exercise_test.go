package main

import "testing"

func TestAbs(t *testing.T) {
	cases := []struct {
		in, want int
	}{
		{-3, 3}, {0, 0}, {4, 4}, {-100, 100},
	}
	for _, c := range cases {
		t.Run("", func(t *testing.T) {
			if got := Abs(c.in); got != c.want {
				t.Fatalf("Abs(%d)=%d want %d", c.in, got, c.want)
			}
		})
	}
}
