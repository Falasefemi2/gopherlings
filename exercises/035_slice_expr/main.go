// 035: Slice expressions share storage: s[1:3] aliases s.
// Full slice expr s[1:3:3] caps capacity to prevent append clobber.
// TODO: append without clobbering the original's tail.
package main

func AppendFirstTwo(s []int, extra int) []int {
	sub := s[:2:2]
	sub = append(sub, extra)
	return sub
}
