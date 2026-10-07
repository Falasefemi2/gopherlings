package main

import (
	"os"
	"testing"
)

func TestEnv(t *testing.T) {
	os.Unsetenv("APP_ENV")
	if Env() != "dev" {
		t.Fatalf("unset should default dev, got %q", Env())
	}
	os.Setenv("APP_ENV", "")
	if Env() != "" {
		t.Fatalf("explicit empty should stay empty, got %q", Env())
	}
	os.Setenv("APP_ENV", "prod")
	if Env() != "prod" {
		t.Fatalf("got %q", Env())
	}
	os.Unsetenv("APP_ENV")
}
