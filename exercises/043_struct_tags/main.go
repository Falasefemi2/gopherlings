// 043: Struct tags are metadata strings; encoding/json reads
// `json:"name"` to map fields. Unexported fields are ignored.
// TODO: make JSON use lowercase keys.
package main

import "encoding/json"

type User struct {
	Name string
	Age  int
}

func ToJSON() string {
	b, _ := json.Marshal(User{Name: "ann", Age: 3})
	return string(b)
}
