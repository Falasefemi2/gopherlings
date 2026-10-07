// 095: CAPSTONE: a tiny CLI: flags in, JSON out. Keep main thin;
// testable funcs return values, main handles flags/os.Exit.
package main

import "fmt"

func Greet(name string) string {
	return fmt.Sprintf("hi %s", name)
}
