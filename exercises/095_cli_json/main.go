// 095 main: parse flags, print JSON. (Edit greet.go for the fix.)
package main

import (
	"flag"
	"fmt"
)

func main() {
	name := flag.String("name", "gopher", "who to greet")
	flag.Parse()
	fmt.Printf("{\"greeting\": \"%s\"}\n", Greet(*name))
}
