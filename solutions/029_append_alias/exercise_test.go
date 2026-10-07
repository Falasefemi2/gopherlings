package main

import (
	"reflect"
	"testing"
)

func TestDoubleAll(t *testing.T) {
	in := []int{1, 2, 3}
	got := DoubleAll(in)
	if !reflect.DeepEqual(got, []int{2, 4, 6}) {
		t.Fatalf("got %v", got)
	}
	if !reflect.DeepEqual(in, []int{1, 2, 3}) {
		t.Fatalf("input was clobbered: %v", in)
	}
}
