// 046: & takes an address, * follows it. Pointers let functions
// mutate callers and avoid copying large values.
// TODO: increment the caller's variable through the pointer.
package main

func Inc(p *int) {
	*p++
}
