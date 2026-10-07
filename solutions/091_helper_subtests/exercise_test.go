package main

import "testing"

func TestDouble2(t *testing.T) {
	CheckEqual(t, Double2([]int{1, 2}), []int{2, 4})
}
