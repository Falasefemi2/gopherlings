// 059: errors.As finds the first error of a target type in the
// chain. Use it for structured errors with extra fields.
package main

import (
	"errors"
	"fmt"
)

type FieldError struct {
	Field string
	Msg   string
}

func (e *FieldError) Error() string { return e.Field + ": " + e.Msg }

func Bad() error { return fmt.Errorf("req: %w", &FieldError{Field: "age", Msg: "neg"}) }

func FieldOf(err error) string {
	var fe *FieldError
	if errors.As(err, &fe) {
		return fe.Field
	}
	return ""
}
