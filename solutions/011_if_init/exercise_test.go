package main

import "testing"

func TestGrade(t *testing.T) {
	if Grade(90) != "pass" {
		t.Fatal("90 should pass")
	}
	if Grade(30) != "fail" {
		t.Fatal("30 should fail")
	}
}
