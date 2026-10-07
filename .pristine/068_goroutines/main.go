// 068: `go f()` runs f concurrently. The caller must wait,
// or results vanish when the function returns. Channels/WaitGroup sync.
// TODO: compute the sum concurrently and wait for it.
package main

func SumAsync(xs []int) int {
	sum := 0
	go func() {
		for _, x := range xs {
			sum += x
		}
	}()
	return sum
}
