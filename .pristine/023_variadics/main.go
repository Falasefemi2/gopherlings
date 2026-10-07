// 023: Variadics take any number of args as a slice: f(nums ...int).
// Call with f(1,2) or f(slice...).
// TODO: return the sum, not the count.
package main

func Sum(nums ...int) int {
	return len(nums)
}
