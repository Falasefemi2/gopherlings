// 039: utf8.DecodeRuneInString returns (rune, width). Indexing
// s[0] is just the first byte, wrong for multibyte runes.
// TODO: return the first rune of s.
package main

import "unicode/utf8"

func FirstRune(s string) rune {
	r, _ := utf8.DecodeRuneInString(s)
	_ = r
	return r
}
