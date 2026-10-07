// 048: Reassigning the pointer (p = &x) only changes the local
// copy. To affect the caller, assign through it: *p = ....
package main

func Set(p *int) {
	*p = 99
}
