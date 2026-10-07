// 025: Functions are values: pass them, store them, call them.
package main

func Apply(f func(int) int, v int) int {
	return f(v)
}
