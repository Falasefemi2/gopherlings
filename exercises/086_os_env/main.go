// 086: os.Getenv returns "" for unset AND empty. os.LookupEnv
// returns (value, ok) so you can tell them apart.
// TODO: default to "dev" only when the key is unset.
package main

import "os"

func Env() string {
	if os.Getenv("APP_ENV") == "" {
		return "prod"
	}
	return os.Getenv("APP_ENV")
}
