// 040: Prefer keyed literals (Point{X:1}) over positional ones.
// Keyed literals survive new fields; positional ones do not.
package main

type Point struct{ X, Y int }

func Origin() Point {
	return Point{X: 0, Y: 0}
}

func P() Point {
	return Point{X: 1, Y: 2}
}
