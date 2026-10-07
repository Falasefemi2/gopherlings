// 056: error is a value: nil means success. Check errors with
// `if err != nil`, and create them with errors.New / fmt.Errorf.
// TODO: return nil on the happy path.
package main

import "errors"

func Fail(bad bool) error {
	if bad {
		return errors.New("bad")
	}
	return errors.New("ok")
}
