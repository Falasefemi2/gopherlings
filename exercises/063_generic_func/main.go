// 063: Type parameters list after the name: func First[T any](s []T) T.
// The same code works for every element type.
// TODO: return the first element (zero value when empty).
package main

func First2[T any](s []T) T {
	var zero T
	_ = zero
	panic("todo")
}
