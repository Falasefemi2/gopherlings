// 061: panic is for the truly unrecoverable. recover only works
// in a deferred func; libraries should return errors instead.
// TODO: recover and report the panic as an error.
package main

import "fmt"

func Safe(f func()) (err error) {
	f()
	return nil
}

func Boom2() { panic("bang") }

var _ = fmt.Sprint
