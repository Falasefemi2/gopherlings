// 082: encoding/json marshals exported fields only. Tags rename keys:
// `json:"name"`. Marshal never fails for simple structs; check errors anyway.
package main

import "encoding/json"

type Person3 struct {
	Name string `json:"name"`
	Age  int    `json:"age"`
}

func Encode() string {
	b, err := json.Marshal(Person3{Name: "ann", Age: 3})
	if err != nil {
		return ""
	}
	return string(b)
}
