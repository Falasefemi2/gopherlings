// 060: errors.Join (Go 1.20+) merges errors; Is/As match any part.
// Useful for validation collecting every problem at once.
package main

import "errors"

var (
	ErrA = errors.New("a")
	ErrB = errors.New("b")
)

func Both() error {
	return errors.Join(ErrA, ErrB)
}
