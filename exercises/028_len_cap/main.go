// 028: len is usable elements; cap is backing-array size.
// make([]int, 2, 5) has len 2, cap 5. append grows up to cap.
// TODO: report the real len and cap.
package main

func LenCap() (int, int) {
	s := make([]int, 2, 5)
	a := len(s)
	b := cap(s)
	return a, b
}
