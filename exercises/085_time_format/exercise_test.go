package main

import (
	"testing"
	"time"
)

func TestDayString(t *testing.T) {
	d := time.Date(2026, 3, 9, 0, 0, 0, 0, time.UTC)
	if DayString(d) != "2026-03-09" {
		t.Fatalf("got %q", DayString(d))
	}
}
