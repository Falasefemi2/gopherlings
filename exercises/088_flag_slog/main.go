// 088: The flag package declares CLI options: p := flag.Int(...).
// Call flag.Parse() before use; defaults apply with no args.
// TODO: print "port=8080" using a flag default (no CLI args needed).
package main

import (
	"flag"
	"fmt"
)

func main() {
	port := flag.Int("port", 1234, "port")
	flag.Parse()
	fmt.Printf("port=%d\n", *port)
}
