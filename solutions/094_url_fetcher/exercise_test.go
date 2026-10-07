package main

import (
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"
	"time"
)

func TestFetchAll(t *testing.T) {
	srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		time.Sleep(60 * time.Millisecond)
		_, _ = w.Write([]byte(strings.Repeat("x", 10)))
	}))
	defer srv.Close()
	urls := []string{srv.URL + "/a", srv.URL + "/b", srv.URL + "/c", srv.URL + "/d"}
	start := time.Now()
	got := FetchAll(urls, 4)
	if time.Since(start) > 150*time.Millisecond {
		t.Fatalf("too slow: fetches look sequential (%v)", time.Since(start))
	}
	for _, u := range urls {
		if got[u] != 10 {
			t.Fatalf("url %s: got %d want 10", u, got[u])
		}
	}
}
