package main

import (
	"reflect"
	"testing"
)

func TestNums(t *testing.T) {
	if got := Nums(); !reflect.DeepEqual(got, []int{1, 2, 3}) {
		t.Fatalf("got %#v", got)
	}
}
