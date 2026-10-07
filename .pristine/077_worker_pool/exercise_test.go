package main

import (
	"reflect"
	"sort"
	"testing"
)

func TestPool(t *testing.T) {
	got := Pool([]int{1, 2, 3, 4, 5})
	sort.Ints(got)
	if !reflect.DeepEqual(got, []int{2, 4, 6, 8, 10}) {
		t.Fatalf("got %v", got)
	}
}
