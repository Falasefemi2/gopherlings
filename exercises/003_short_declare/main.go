// 003: := declares AND assigns; a second := with no new variable
// on the left is a compile error. = assigns to an existing variable.
// TODO: fix the compile error so the program prints: b
package main

import "fmt"

func main() {
	name := "a"
	name = "b"
	fmt.Println(name)
}
