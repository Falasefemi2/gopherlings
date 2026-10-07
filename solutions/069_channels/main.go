// 069: Channels move values between goroutines. Senders usually
// close when done; receivers range until close.
package main

func Produce() []int {
	ch := make(chan int)
	go func() {
		for i := 1; i <= 3; i++ {
			ch <- i
		}
		close(ch)
	}()
	var out []int
	for v := range ch {
		out = append(out, v)
	}
	return out
}
