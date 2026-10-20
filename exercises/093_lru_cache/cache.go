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
	return &LRU{
		cap:   capacity,
		items: make(map[string]*list.Element),
		order: list.New(),
	}
}

func (c *LRU) Get(key string) (int, bool) {
	if el, ok := c.items[key]; ok {
		c.order.MoveToFront(el)
		return el.Value.(entry).val, true
	}
	return 0, false
}

func (c *LRU) Put(key string, val int) {
	if c.cap <= 0 {
		return
	}

	if el, ok := c.items[key]; ok {
		el.Value = entry{key, val}
		c.order.MoveToFront(el)
		return
	}

	el := c.order.PushFront(entry{key, val})
	c.items[key] = el

	if c.order.Len() > c.cap {
		oldest := c.order.Back()
		if oldest != nil {
			oldEntry := oldest.Value.(entry)
			delete(c.items, oldEntry.key)
			c.order.Remove(oldest)
		}
	}
}
