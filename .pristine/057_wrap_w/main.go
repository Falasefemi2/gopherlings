// 057: Wrap with fmt.Errorf("...: %w", err) to keep the chain.
// %v formats but breaks Is/As. Add context at each layer.
// TODO: wrap so errors.Is still finds the sentinel.
package main

import (
	"errors"
	"fmt"
)

var ErrBase = errors.New("base")

func Middle() error {
	return fmt.Errorf("middle: %v", ErrBase)
}
