// 012: switch picks the first matching case. No break needed.
// TODO: return the short day names below.
package main

func Day(n int) string {
	switch n {
	case 1:
		return "Mon"
	case 2:
		return "Tue"
	default:
		return "?"
	}
}
