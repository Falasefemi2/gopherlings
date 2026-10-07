// 036: string is bytes; len counts bytes, not characters (runes).
// range decodes UTF-8 runes; indexing gives single bytes.
package main

func RuneLen(s string) int {
	n := 0
	for range s {
		n++
	}
	return n
}
