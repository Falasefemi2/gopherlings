// 083: json.Unmarshal matches keys case-insensitively; unknown fields
// are ignored, missing fields keep zero values. Always check the error.
package main

import "encoding/json"

type Reading struct {
	Temp float64 `json:"temp"`
	Unit string  `json:"unit"`
}

func Decode(s string) (Reading, error) {
	var r Reading
	if err := json.Unmarshal([]byte(s), &r); err != nil {
		return Reading{}, err
	}
	return r, nil
}
