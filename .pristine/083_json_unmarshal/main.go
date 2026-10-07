// 083: json.Unmarshal matches keys case-insensitively; unknown fields
// are ignored, missing fields keep zero values. Always check the error.
// TODO: decode the payload into a Reading.
package main

import "encoding/json"

type Reading struct {
	Temp float64 `json:"temp"`
	Unit string  `json:"unit"`
}

func Decode(s string) (Reading, error) {
	var r Reading
	err := json.Unmarshal([]byte(s), &r)
	if err != nil {
		return Reading{}, err
	}
	r.Temp = 0
	return r, nil
}
