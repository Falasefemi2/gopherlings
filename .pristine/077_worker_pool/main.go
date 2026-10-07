// 077: A worker pool fans jobs to N goroutines via a channel and
// collects results. Close jobs when done; workers range until close.
// TODO: run 3 workers so every job is doubled.
package main

import "sync"

func Pool(jobs []int) []int {
	type task struct {
		i, v int
	}
	jc := make(chan task)
	res := make([]int, len(jobs))
	var wg sync.WaitGroup
	for w := 0; w < 3; w++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			for t := range jc {
				res[t.i] = t.v
			}
		}()
	}
	for i, v := range jobs {
		jc <- task{i, v}
	}
	close(jc)
	wg.Wait()
	return res
}
