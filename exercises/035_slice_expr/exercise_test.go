package main

import (
	"reflect"
	"testing"
)

func TestAppendFirstTwo(t *testing.T) {
	s := []int{1, 2, 3}
	got := AppendFirstTwo(s, 9)

	if !reflect.DeepEqual(got, []int{1, 2, 9}) {
		t.Fatalf("got %v", got)
	}
	if !reflect.DeepEqual(s, []int{1, 2, 3}) {
		t.Fatalf("source clobbered: %v", s)
	}
}
