// 013: Go cases do NOT fall through; the keyword fallthrough is
// opt-in and usually a smell.
package main

func Letter(score int) string {
	switch {
	case score >= 90:
		return "A"
	case score >= 80:
		return "B"
	case score >= 70:
		return "C"
	default:
		return "F"
	}
}
