// 063: Type parameters list after the name: func First[T any](s []T) T.
// The same code works for every element type.
package main

func First2[T any](s []T) T {
	if len(s) == 0 {
		var zero T
		return zero
	}
	return s[0]
}
