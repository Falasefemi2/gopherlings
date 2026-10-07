// 038: strconv converts text<->numbers: Atoi, Itoa, ParseInt,
// ParseFloat, Quote. Most return (value, error); check it.
package main

import "strconv"

func ParseAge(s string) (int, error) {
	return strconv.Atoi(s)
}
