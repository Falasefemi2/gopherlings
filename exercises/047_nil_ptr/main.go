// 047: The zero value of any pointer is nil. Dereferencing nil
// panics; always check before following.
// TODO: return 0 for nil instead of panicking.
package main

func Deref(p *int) int {
	if p == nil {
		return 0
	}
	return *p
}
