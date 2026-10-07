// 008: Go never converts implicitly. string(65) is "A" (rune),
// not "65". Use strconv for decimal text.
// TODO: return the decimal text of n.
package main

func Itoa(n int) string {
	return string(n)
}
