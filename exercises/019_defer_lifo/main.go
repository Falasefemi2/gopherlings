// 019: defer schedules a call for when the function returns.
// Deferred calls run LIFO: last deferred, first executed.
// TODO: print 321 using three deferred Print calls.
package main

import "fmt"

func main() {
	defer fmt.Print(1)
	defer fmt.Print(2)
	defer fmt.Print(3)
	fmt.Println()
}
