// 071: select waits on many channels; first ready wins. Combine
// with time.After for timeouts, default for non-blocking.
package main

import "time"

func Race(fast, slow <-chan string) string {
	select {
	case s := <-fast:
		return s
	case s := <-slow:
		return s
	case <-time.After(2 * time.Second):
		return "timeout"
	}
}
