// 026: Methods are functions with a receiver. A method value like
// f := c.Inc keeps the receiver bound; pointer receivers mutate.
package main

type Counter2 struct{ N int }

func (c *Counter2) Inc() { c.N++ }

func TwoIncs() int {
	c := &Counter2{}
	f := c.Inc
	f()
	f()
	return c.N
}
