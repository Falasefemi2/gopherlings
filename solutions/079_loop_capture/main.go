// 079: GOTCHA: closures share the variables they capture. (Go 1.22
// made loop vars per-iteration, but an outer variable is still shared.)
// Pass the value as a parameter to capture it.
package main

func Closures() []int {
	var fns []func() int
	i := 0
	for ; i < 3; i++ {
		fns = append(fns, func(v int) func() int {
			return func() int { return v }
		}(i))
	}
	out := []int{fns[0](), fns[1](), fns[2]()}
	return out
}
