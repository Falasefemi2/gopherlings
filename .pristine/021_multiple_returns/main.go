// 021: Functions can return several values: func f() (int, error).
// Comma-separated returns power the (value, error) idiom.
// TODO: return host first, then port.
package main

import "strings"

func SplitHostPort(s string) (string, string) {
	parts := strings.SplitN(s, ":", 2)
	if len(parts) != 2 {
		return "", ""
	}
	return parts[1], parts[0]
}
