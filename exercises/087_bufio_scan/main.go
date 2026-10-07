// 087: bufio.Scanner splits input (lines by default). Loop with
// Scan(), read with Text(), and check Scanner.Err() afterwards.
// TODO: count the lines.
package main

import (
	"bufio"
	"strings"
)

func Lines(s string) int {
	sc := bufio.NewScanner(strings.NewReader(s))
	n := 0
	for sc.Scan() {
		n += len(sc.Text())
	}
	return n
}
