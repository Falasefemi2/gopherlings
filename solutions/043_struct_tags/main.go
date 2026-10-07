// 043: Struct tags are metadata strings; encoding/json reads
// `json:"name"` to map fields. Unexported fields are ignored.
package main

import "encoding/json"

type User struct {
	Name string `json:"name"`
	Age  int    `json:"age"`
}

func ToJSON() string {
	b, _ := json.Marshal(User{Name: "ann", Age: 3})
	return string(b)
}
