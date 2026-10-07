// 052: GOTCHA: an interface holding a typed nil pointer is NOT
// nil itself. Return explicit nil instead of a nil pointer.
// TODO: return nil error on success.
package main

type Boom struct{}

func (b *Boom) Error() string { return "boom" }

func Check(ok bool) error {
	var b *Boom
	if ok {
		return b
	}
	_ = b
	return b
}
