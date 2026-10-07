// 008: Go never converts implicitly. string(65) is "A" (rune),
// not "65". Use strconv for decimal text.
package main

import "strconv"

func Itoa(n int) string {
	return strconv.Itoa(n)
}
