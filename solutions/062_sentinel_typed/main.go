// 062: Sentinels (var ErrX) suit fixed cases; typed errors suit
// dynamic context. Callers use Is for the first, As for the second.
package main

import "errors"

var ErrMissing = errors.New("missing")

type BadValue struct{ V string }

func (e *BadValue) Error() string { return "bad:" + e.V }

func Classify(v string) error {
	if v == "" {
		return ErrMissing
	}
	return &BadValue{V: v}
}
