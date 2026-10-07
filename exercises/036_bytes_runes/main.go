// 036: string is bytes; len counts bytes, not characters (runes).
// range decodes UTF-8 runes; indexing gives single bytes.
// TODO: count characters (runes), not bytes.
package main

func RuneLen(s string) int {
	return len(s)
}
