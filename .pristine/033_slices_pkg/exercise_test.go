package main

import (
	"reflect"
	"testing"
)

func TestSorted(t *testing.T) {
	if got := Sorted([]int{3, 1, 2}); !reflect.DeepEqual(got, []int{1, 2, 3}) {
		t.Fatalf("got %v", got)
	}
}
