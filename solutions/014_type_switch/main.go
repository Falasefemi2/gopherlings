// 014: A type switch branches on dynamic type safely:
// switch x := v.(type) { case string: ... case int: ... }.
package main

import "fmt"

func Describe(v any) string {
	switch x := v.(type) {
	case string:
		return "str:" + x
	case int:
		return fmt.Sprintf("int:%d", x)
	default:
		return "?"
	}
}
