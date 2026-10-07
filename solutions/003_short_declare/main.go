// 003: := declares AND assigns; a second := with no new variable
// on the left is a compile error. = assigns to an existing variable.
package main

import "fmt"

func main() {
	name := "a"
	name = "b"
	fmt.Println(name)
}
