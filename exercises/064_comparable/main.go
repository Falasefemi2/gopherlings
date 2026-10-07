// 064: comparable constrains to types supporting ==/!=, so maps
// and dedup can use it. any does not allow ==.
// TODO: constrain T so == compiles.
package main

func Has[T any](s []T, v T) bool {
	for _, x := range s {
		if x == v {
			return true
		}
	}
	return false
}
