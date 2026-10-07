// 041: Value receivers copy; pointer receivers mutate. Use pointer
// for mutation or large structs, value for small immutable ones.
// TODO: make Scale actually scale the rectangle.
package main

type Rect struct{ W, H int }

func (r Rect) Scale(k int) { r.W *= k; r.H *= k }

func Scaled() Rect {
	r := Rect{W: 2, H: 3}
	r.Scale(10)
	return r
}
