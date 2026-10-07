// 011: if can run a short statement before the condition, scoped
// to the branches: if s := score; s >= 60 { ... }.
package main

func Grade(score int) string {
	if s := score; s >= 60 {
		return "pass"
	}
	return "fail"
}
