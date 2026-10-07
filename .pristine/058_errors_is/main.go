// 058: errors.Is walks the wrap chain. == only matches the exact
// value, so wrapped sentinels need Is.
// TODO: detect ErrGone even when wrapped.
package main

import (
	"errors"
	"fmt"
)

var ErrGone = errors.New("gone")

func Gone() error { return fmt.Errorf("op: %w", ErrGone) }

func IsGone(err error) bool { return err == ErrGone }
