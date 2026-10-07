// 028: len is usable elements; cap is backing-array size.
// make([]int, 2, 5) has len 2, cap 5. append grows up to cap.
package main

func LenCap() (int, int) {
	s := make([]int, 2, 5)
	return len(s), cap(s)
}
