// 009: fmt verbs are typed: %d for ints, %s for strings, %v for
// anything, %q for quoted strings. Wrong verbs show up in output.
// TODO: print exactly: answer: 42
package main

import "fmt"

func main() {
	fmt.Printf("answer: %d\n", 42)
}
