// 031: Map lookup returns (value, ok). ok reports presence;
// without it a missing key looks like a stored zero value.
// TODO: report whether the key exists.
package main

func Lookup(m map[string]int, k string) (int, bool) {
	v, ok := m[k]
	return v, ok
}
