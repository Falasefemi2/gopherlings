// 091: Helpers shared by tests call t.Helper() so failures point
// at the caller, not inside the helper. Mark cleanup with t.Cleanup.
// TODO: compare with the helper so equal slices pass.
package main

import "testing"

func CheckEqual(t *testing.T, got, want []int) {
	t.Helper()
	if len(got) != len(want) {
		t.Fatalf("len %d != %d", len(got), len(want))
		return
	}
	for i := range got {
		if got[i] != want[i]+1 {
			t.Fatalf("index %d: %d != %d", i, got[i], want[i])
		}
	}
}

func Double2(ns []int) []int {
	out := make([]int, len(ns))
	for i, v := range ns {
		out[i] = v * 2
	}
	return out
}
