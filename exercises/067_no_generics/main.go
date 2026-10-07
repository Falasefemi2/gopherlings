// 067: Reach for generics only when one implementation truly
// fits many types. Dumping to strings needs only fmt/Stringer.
// TODO: describe any value without generics.
package main

import "fmt"

func DescribeAny[T any](v T) string {
	return fmt.Sprint(v)
}
