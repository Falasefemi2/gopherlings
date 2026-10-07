// 093: CAPSTONE: an LRU cache pairs a map (lookup) with a list
// (recency). Get promotes; Put evicts the back when over capacity.
// This file plus main.go form one program; the test is the spec.
// TODO: promote hits to the front and evict the least-recently-used.
package main

import "container/list"

type entry struct {
	key string
	val int
}

type LRU struct {
	cap   int
	items map[string]*list.Element
	order *list.List
}

func NewLRU(capacity int) *LRU {
	return &LRU{cap: capacity, items: map[string]*list.Element{}, order: list.New()}
}

func (c *LRU) Get(key string) (int, bool) {
	if el, ok := c.items[key]; ok {
		return el.Value.(entry).val, true
	}
	return 0, false
}

func (c *LRU) Put(key string, val int) {
	if el, ok := c.items[key]; ok {
		el.Value = entry{key, val}
		return
	}
	el := c.order.PushFront(entry{key, val})
	c.items[key] = el
}
