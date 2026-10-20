// 071: select waits on many channels; first ready wins. Combine
// with time.After for timeouts, default for non-blocking.
// TODO: return "fast" or "slow" depending on which answers first.
package main

import "time"

func Race(fast, slow <-chan string) string {
	select {
	case msg1 := <-fast:
		return msg1
	case msg2 := <-slow:
		return msg2
	case <-time.After(5 * time.Millisecond):
		return "timeout"
	}
}
