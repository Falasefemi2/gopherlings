// 056: error is a value: nil means success. Check errors with
// `if err != nil`, and create them with errors.New / fmt.Errorf.
package main

import "errors"

func Fail(bad bool) error {
	if bad {
		return errors.New("bad")
	}
	return nil
}
