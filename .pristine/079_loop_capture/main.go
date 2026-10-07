// 079: GOTCHA: closures share the variables they capture. (Go 1.22
// made loop vars per-iteration, but an outer variable is still shared.)
// Here i lives OUTSIDE the loop, so every func sees the final value.
// TODO: capture each iteration's value.
package main

func Closures() []int {
	var fns []func() int
	i := 0
	for ; i < 3; i++ {
		fns = append(fns, func() int { return i })
	}
	out := []int{fns[0](), fns[1](), fns[2]()}
	return out
}
