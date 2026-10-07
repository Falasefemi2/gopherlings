package main

import (
	"reflect"
	"testing"
)

func TestClosures(t *testing.T) {
	if got := Closures(); !reflect.DeepEqual(got, []int{0, 1, 2}) {
		t.Fatalf("got %v want [0 1 2]", got)
	}
}
