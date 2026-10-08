// 027: Arrays have fixed length ([3]int); slices are views over
// arrays and can grow. Most Go code uses slices ([]int).
// TODO: return the slice 1..3 with length 3.
package main

func Nums() []int {
	a := [3]int{1, 2, 3}
	b := a[0:3]
	return b
}
