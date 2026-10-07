// 023: Variadics take any number of args as a slice: f(nums ...int).
// Call with f(1,2) or f(slice...).
package main

func Sum(nums ...int) int {
	total := 0
	for _, n := range nums {
		total += n
	}
	return total
}
