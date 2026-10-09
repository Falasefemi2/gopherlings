// 048: Reassigning the pointer (p = &x) only changes the local
// copy. To affect the caller, assign through it: *p = ....
// TODO: set the caller's value to 99.
package main

func Set(p *int) {
	x := 99
	*p = x
}
