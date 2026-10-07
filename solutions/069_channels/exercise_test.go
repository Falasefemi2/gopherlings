package main

import (
	"reflect"
	"testing"
	"time"
)

func TestProduce(t *testing.T) {
	done := make(chan []int, 1)
	go func() { done <- Produce() }()
	select {
	case got := <-done:
		if !reflect.DeepEqual(got, []int{1, 2, 3}) {
			t.Fatalf("got %v", got)
		}
	case <-time.After(500 * time.Millisecond):
		t.Fatal("deadlock: channel never closed, range never ends")
	}
}
