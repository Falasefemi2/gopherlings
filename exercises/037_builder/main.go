// 037: strings.Builder concatenates without O(n^2) copies.
// WriteString in a loop, then String() once.
// TODO: join the parts efficiently.
package main

func Join(parts []string) string {
	s := ""
	for _, p := range parts {
		s += p
	}
	_ = s
	return "TODO"
}
