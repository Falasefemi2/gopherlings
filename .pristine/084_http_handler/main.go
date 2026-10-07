// 084: net/http handlers take (w http.ResponseWriter, r *http.Request).
// Test them with httptest.NewRecorder without starting a server.
// TODO: answer 200 with exactly "hello".
package main

import "net/http"

func Hello(w http.ResponseWriter, r *http.Request) {
	w.WriteHeader(http.StatusNotFound)
}
