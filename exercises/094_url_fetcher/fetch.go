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
	out := make(map[string]int)
	var mu sync.Mutex
	var wg sync.WaitGroup

	if limit <= 0 {
		return out
	}

	sem := make(chan struct{}, limit)

	for _, u := range urls {
		wg.Add(1)

		go func(u string) {
			defer wg.Done()

			// Acquire a semaphore slot.
			sem <- struct{}{}
			defer func() {
				<-sem
			}()

			resp, err := http.Get(u)
			if err != nil {
				mu.Lock()
				out[u] = -1
				mu.Unlock()
				return
			}
			defer resp.Body.Close()

			body, err := io.ReadAll(resp.Body)

			mu.Lock()
			if err != nil {
				out[u] = -1
			} else {
				out[u] = len(body)
			}
			mu.Unlock()
		}(u)
	}

	wg.Wait()
	return out
}
