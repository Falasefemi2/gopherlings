// 061: panic is for the truly unrecoverable. recover only works
// in a deferred func; libraries should return errors instead.
package main

import "fmt"

func Safe(f func()) (err error) {
	defer func() {
		if r := recover(); r != nil {
			err = fmt.Errorf("panic: %v", r)
		}
	}()
	f()
	return nil
}

func Boom2() { panic("bang") }
