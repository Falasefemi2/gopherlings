// 093 demo entrypoint (not used by the test).
package main

func demoLRU() {
	c := NewLRU(2)
	c.Put("a", 1)
	c.Put("b", 2)
	_, _ = c.Get("a")
}
