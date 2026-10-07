// 052: GOTCHA: an interface holding a typed nil pointer is NOT
// nil itself. Return explicit nil instead of a nil pointer.
package main

type Boom struct{}

func (b *Boom) Error() string { return "boom" }

func Check(ok bool) error {
	if ok {
		return nil
	}
	return &Boom{}
}
