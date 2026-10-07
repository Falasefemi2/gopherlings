// 068: `go f()` runs f concurrently. The caller must wait,
// or results vanish when the function returns. Channels/WaitGroup sync.
package main

func SumAsync(xs []int) int {
	done := make(chan int, 1)
	go func() {
		sum := 0
		for _, x := range xs {
			sum += x
		}
		done <- sum
	}()
	return <-done
}
