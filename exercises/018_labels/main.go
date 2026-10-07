// 018: Labels let break/continue target an outer loop:
// outer: for ... { for ... { break outer } }.
// TODO: stop both loops once the target is found.
package main

func Find(target int, m [][]int) (int, int, bool) {
	for i := range m {
		for j := range m[i] {
			if m[i][j] == target {
				break
			}
		}
	}
	return 0, 0, false
}
