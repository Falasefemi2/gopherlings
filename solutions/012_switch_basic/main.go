// 012: switch picks the first matching case. No break needed.
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
