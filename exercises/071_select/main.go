// 071: select waits on many channels; first ready wins. Combine
// with time.After for timeouts, default for non-blocking.
// TODO: return "fast" or "slow" depending on which answers first.
package main

import "time"

func Race(fast, slow <-chan string) string {
	time.Sleep(5 * time.Millisecond)
	return <-slow
}
