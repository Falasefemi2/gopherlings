// 010: const values cannot be reassigned; use var (or :=)
// for things that change.
package main

import "fmt"

func main() {
	var x = 1
	x = 2
	fmt.Println(x)
}
