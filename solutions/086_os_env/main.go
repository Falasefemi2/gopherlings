// 086: os.Getenv returns "" for unset AND empty. os.LookupEnv
// returns (value, ok) so you can tell them apart.
package main

import "os"

func Env() string {
	if v, ok := os.LookupEnv("APP_ENV"); ok {
		return v
	}
	return "dev"
}
