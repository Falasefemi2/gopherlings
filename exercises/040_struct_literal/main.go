// 040: Prefer keyed literals (Point{X:1}) over positional ones.
// Keyed literals survive new fields; positional ones do not.
// TODO: build Point{X:1, Y:2} with field names.
package main

type Point struct{ X, Y int }

func Origin() Point {
	return Point{0, 0}
}

func P() Point {
	return Point{2, 1}
}
