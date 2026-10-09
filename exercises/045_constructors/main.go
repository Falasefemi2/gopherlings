// 045: Idiom: NewT validates and returns (*T, error). Zero value
// should be useful; constructors enforce invariants.
// TODO: reject empty names with an error.
package main

import "errors"

type Account struct{ Name string }

func NewAccount(name string) (*Account, error) {
	if name == "" {
		return &Account{}, ErrName
	}
	return &Account{Name: name}, nil
}

var ErrName = errors.New("bad name")
