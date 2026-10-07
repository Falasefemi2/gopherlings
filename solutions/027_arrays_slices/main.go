// 027: Arrays have fixed length ([3]int); slices are views over
// arrays and can grow. Most Go code uses slices ([]int).
package main

func Nums() []int {
	return []int{1, 2, 3}
}
