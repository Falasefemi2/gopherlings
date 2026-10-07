// 046: & takes an address, * follows it. Pointers let functions
// mutate callers and avoid copying large values.
package main

func Inc(p *int) {
	*p++
}
