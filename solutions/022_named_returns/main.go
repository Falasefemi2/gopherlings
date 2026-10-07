// 022: Named results are pre-declared locals; bare `return`
// returns them as-is. Use for short funcs, not as documentation.
package main

func Swap(a, b int) (x, y int) {
	x = b
	y = a
	return
}
