// 004: Every type has a zero value used when no value is given:
// 0 for numbers, "" for strings, false for bools, nil for the rest.
// TODO: return the zero values instead of these placeholders.
package main

func Zero() (int, string, bool) {
	return 0, "", false
}
