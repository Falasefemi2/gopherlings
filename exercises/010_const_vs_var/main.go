// 010: const values cannot be reassigned; use var (or :=)
// for things that change. TODO: fix the error; print 2.
package main

import "fmt"

func main() {
	x := 1
	x = 2
	fmt.Println(x)
}
