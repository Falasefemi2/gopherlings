package main

import (
	"reflect"
	"testing"
)

func TestFirst(t *testing.T) {
	if got := First(4); !reflect.DeepEqual(got, []int{0, 1, 2, 3}) {
		t.Fatalf("got %v", got)
	}
}
