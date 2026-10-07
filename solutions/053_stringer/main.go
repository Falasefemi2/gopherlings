// 053: Implement fmt.Stringer (String() string) to control how
// fmt prints your type. It is used by Println, %v and %s.
package main

import "fmt"

type Person struct{ Name string }

func (p Person) String() string { return "user:" + p.Name }

func Greet2(p Person) string { return fmt.Sprint(p) }
