// 014: A type switch branches on dynamic type safely:
// switch x := v.(type) { case string: ... case int: ... }.
// TODO: handle both string and int without panicking.
package main

import "fmt"

func Describe(v any) string {
	switch s := v.(type) {
	case string:
		return "str:" + s
	case int:
		return fmt.Sprintf("int:%d", s)
	default:
		return "unknown"
	}
}
