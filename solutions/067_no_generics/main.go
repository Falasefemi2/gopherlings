// 067: Reach for generics only when one implementation truly
// fits many types. Dumping to strings needs only fmt/Stringer.
package main

import "fmt"

func DescribeAny(v any) string {
	return fmt.Sprintf("%v (%T)", v, v)
}
