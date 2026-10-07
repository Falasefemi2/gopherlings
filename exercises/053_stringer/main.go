// 053: Implement fmt.Stringer (String() string) to control how
// fmt prints your type. It is used by Println, %v and %s.
// TODO: format as "user:<name>".
package main

import "fmt"

type Person struct{ Name string }

func Greet2(p Person) string { return fmt.Sprint(p) }
