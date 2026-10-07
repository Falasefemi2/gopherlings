// 018: Labels let break/continue target an outer loop:
// outer: for ... { for ... { break outer } }.
package main

func Find(target int, m [][]int) (int, int, bool) {
	fr, fc := 0, 0
	found := false
outer:
	for i := range m {
		for j := range m[i] {
			if m[i][j] == target {
				fr, fc, found = i, j, true
				break outer
			}
		}
	}
	return fr, fc, found
}
