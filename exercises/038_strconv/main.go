// 038: strconv converts text<->numbers: Atoi, Itoa, ParseInt,
// ParseFloat, Quote. Most return (value, error); check it.
// TODO: parse the decimal string, returning errors properly.
package main

import "strconv"

func ParseAge(s string) (int, error) {
	n, _ := strconv.Atoi(s)
	return n, nil
}
