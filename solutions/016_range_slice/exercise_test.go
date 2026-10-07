package main

import (
	"reflect"
	"testing"
)

func TestDouble(t *testing.T) {
	if got := Double([]int{1, 2, 3}); !reflect.DeepEqual(got, []int{2, 4, 6}) {
		t.Fatalf("got %v", got)
	}
}
