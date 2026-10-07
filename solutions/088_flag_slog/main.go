// 088: The flag package declares CLI options: p := flag.Int(...).
// Call flag.Parse() before use; defaults apply with no args.
package main

import (
	"flag"
	"fmt"
)

func main() {
	port := flag.Int("port", 8080, "port")
	flag.Parse()
	fmt.Printf("port=%d\n", *port)
}
