// 085: Go formats time with the reference layout Mon Jan 2 15:04:05
// MST 2006 (01/02 03:04:05PM '06 -0700). Use time.Date, not strings.
// TODO: format as "2026-01-02".
package main

import "time"

func DayString(t time.Time) string {
	return t.Format("02-01-2006")
}
