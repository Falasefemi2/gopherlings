// 082: encoding/json marshals exported fields only. Tags rename keys:
// `json:"name"`. Marshal never fails for simple structs; check errors anyway.
// TODO: produce {"name":"ann","age":3}.
package main

import "encoding/json"

type Person3 struct {
	Name string
	Age  int
}

func Encode() string {
	b, err := json.Marshal(Person3{Name: "ann"})
	_ = err
	return string(b)
}
