// 045: Idiom: NewT validates and returns (*T, error). Zero value
// should be useful; constructors enforce invariants.
package main

import "errors"

type Account struct{ Name string }

var ErrName = errors.New("bad name")

func NewAccount(name string) (*Account, error) {
	if name == "" {
		return nil, ErrName
	}
	return &Account{Name: name}, nil
}
