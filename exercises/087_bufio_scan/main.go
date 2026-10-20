// 087: bufio.Scanner splits input (lines by default). Loop with
// Scan(), read with Text(), and check Scanner.Err() afterwards.
// TODO: count the lines.
package main

import (
	"bufio"
	"fmt"
	"strings"
)

func Lines(s string) int {
	sc := bufio.NewScanner(strings.NewReader(s))
	n := 0
	for sc.Scan() {
		n++
	}
	if err := sc.Err(); err != nil {
		fmt.Println("Error", err)
	}
	return n
}
