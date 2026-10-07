// 066: Generic types take parameters too: type Stack[T any].
// Methods use the same T; zero value of T is the default.
// TODO: Push/Pop in LIFO order.
package main

type Stack[T any] struct{ items []T }

func (s *Stack[T]) Push(v T) { s.items = append(s.items, v) }

func (s *Stack[T]) Pop() (T, bool) {
	var zero T
	if len(s.items) == 0 {
		return zero, false
	}
	v := s.items[0]
	s.items = s.items[1:]
	return v, true
}
