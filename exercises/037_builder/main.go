// 037: strings.Builder concatenates without O(n^2) copies.
// WriteString in a loop, then String() once.
// TODO: join the parts efficiently.
package main

import "strings"

func Join(parts []string) string {
	if len(parts) == 0 {
		return ""
	}
	totalLen := 0
	for _, p := range parts {
		totalLen += len(p)
	}
	var builder strings.Builder
	builder.Grow(totalLen)
	for _, p := range parts {
		builder.WriteString(p)
	}
	return builder.String()
}
