// 037: strings.Builder concatenates without O(n^2) copies.
// WriteString in a loop, then String() once.
package main

import "strings"

func Join(parts []string) string {
	var b strings.Builder
	for _, p := range parts {
		b.WriteString(p)
	}
	return b.String()
}
