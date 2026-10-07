// 094: CAPSTONE: fetch URLs concurrently with at most `limit`
// in flight (semaphore channel), collecting per-URL errors by hand.
// TODO: bound concurrency, wait for all, and record errors.
package main

import (
	"io"
	"net/http"
	"sync"
)

func FetchAll(urls []string, limit int) map[string]int {
	out := map[string]int{}
	var mu sync.Mutex
	for _, u := range urls {
		resp, err := http.Get(u)
		if err != nil {
			continue
		}
		body, _ := io.ReadAll(resp.Body)
		resp.Body.Close()
		mu.Lock()
		out[u] = len(body)
		mu.Unlock()
	}
	return out
}

var _ = sync.WaitGroup{}
