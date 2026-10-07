package main

import (
	"reflect"
	"testing"
)

func TestKeys(t *testing.T) {
	m := map[string]int{"h": 8, "e": 5, "c": 3, "a": 1, "d": 4, "b": 2, "g": 7, "f": 6}
	if got := Keys(m); !reflect.DeepEqual(got, []string{"a", "b", "c", "d", "e", "f", "g", "h"}) {
		t.Fatalf("got %v", got)
	}
}
