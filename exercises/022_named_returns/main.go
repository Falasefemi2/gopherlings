// 022: Named results are pre-declared locals; bare `return`
// returns them as-is. Use for short funcs, not as documentation.
// TODO: actually swap a and b.
package main

func Swap(a, b int) (int, int) {
	return b, a
}
