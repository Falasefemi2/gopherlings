// 095 main: parse flags, print JSON. (Edit greet.go for the fix.)
package main

import (
	"flag"
	"fmt"
)

func main() {
	name := flag.String("name", "", "who to greet")
	flag.Parse()
	if *name == "" {
		*name = "stranger"
	}
	fmt.Printf("{\"greeting\": \"%s\"}\n", Greet(*name))
}
