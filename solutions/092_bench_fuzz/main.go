// 092: Benchmarks (BenchmarkX) time hot paths: `go test -bench=.`.
// Fuzzing (FuzzY) explores inputs: `go test -fuzz=FuzzReverse`.
package main

import "testing"

func Reverse(s string) string {
	r := []rune(s)
	for i, j := 0, len(r)-1; i < j; i, j = i+1, j-1 {
		r[i], r[j] = r[j], r[i]
	}
	return string(r)
}

func BenchmarkReverse(b *testing.B) {
	for i := 0; i < b.N; i++ {
		Reverse("hello world, this is a benchmark")
	}
}

func FuzzReverse(f *testing.F) {
	f.Add("hello")
	f.Fuzz(func(t *testing.T, s string) {
		if Reverse(Reverse(s)) != s {
			t.Fatalf("double reverse failed for %q", s)
		}
	})
}
