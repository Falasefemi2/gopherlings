// 006: Go treats unused local variables as an error, not a warning.
// It keeps code honest. TODO: fix the compile error; print answer: 42
package main

import "fmt"

func main() {
	x := 42
	fmt.Println("answer:", x)
}
