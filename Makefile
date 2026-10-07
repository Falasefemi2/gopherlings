.PHONY: run watch verify test vet list

run:
	go run ./cmd/gopherlings

watch:
	go run ./cmd/gopherlings --watch

verify:
	go run ./cmd/gopherlings --verify-solutions

test:
	go test ./solutions/...

vet:
	go vet ./cmd/... ./solutions/...

list:
	go run ./cmd/gopherlings --list
