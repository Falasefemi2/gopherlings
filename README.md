# Gopherlings

Small, intentionally broken Go programs. Fix them until they compile and pass.
Modeled on Ziglings/Rustlings: the exercises are the teacher, not a tutorial.

For experienced developers learning Go: idioms, the type system, errors,
concurrency, tooling, and where Go differs from what you already know.

Requires Go 1.22+, standard library only, zero dependencies.

## Start here

```sh
cd gopherlings
go run ./cmd/gopherlings --watch
```

Open the file it shows you (e.g. `exercises/001_hello_world/main.go`),
read the header comment, fix the `TODO`, save, and the runner re-checks.
It stops at the first failing exercise; earlier ones already pass.

## The runner

```sh
go run ./cmd/gopherlings                  # check in order, stop at first failure
go run ./cmd/gopherlings --hint           # also print the failing exercise's hint
go run ./cmd/gopherlings --only 29        # check one exercise (id or dir)
go run ./cmd/gopherlings --list           # all exercises with status
go run ./cmd/gopherlings --reset 29       # restore exercise 29 from .pristine/
go run ./cmd/gopherlings --verify-solutions  # maintainer mode (see below)
```

- Progress is derived by actually running everything; no state file to drift.
- `run`-mode exercises check program output; `test`-mode runs `go test`.
- Compiler errors print raw: Go's messages are part of the learning.
- Exit code is non-zero when an exercise fails, so CI can use it.
- Colors disable with `NO_COLOR=1`. `--watch` polls mtimes (stdlib only).

To skip ahead, just open a later file; `--reset N` undoes your edits.
`solutions/` holds working versions for `--verify-solutions` and CI;
don't peek during normal runs.

## Curriculum (95 exercises)

| # | Topic | Contents |
|---|-------|----------|
| 001–010 | Basics | packages, fmt, var vs :=, zero values, iota, unused errors, conversions, verbs, const |
| 011–020 | Control flow | if-init, switch, fallthrough, type switches, for, range (incl. over int), labels, defer |
| 021–026 | Functions | multiple/named returns, variadics, closures, func values, method values |
| 027–035 | Collections | arrays vs slices, len/cap, aliasing, nil maps, comma-ok, map order, slices/maps pkgs |
| 036–039 | Strings | bytes vs runes, Builder, strconv, UTF-8 |
| 040–045 | Structs | literals, receivers, embedding, tags, comparability, constructors |
| 046–048 | Pointers | & vs *, nil, mutation through pointers |
| 049–055 | Interfaces | implicit satisfaction, any, assertions, nil-interface trap, Stringer, Reader |
| 056–062 | Errors | values, %w, Is/As, Join, panic/recover, sentinel vs typed |
| 063–067 | Generics | type params, comparable, cmp.Ordered, generic types, when not to |
| 068–081 | Concurrency | goroutines, channels, select, WaitGroup, Mutex, atomic, context, pools, fan-in, capture, errgroup-by-hand, unclosed channels |
| 082–089 | Stdlib | json, http+httptest, time, os, bufio, flag, sort |
| 090–092 | Testing | table tests, helpers+subtests, benchmarks+fuzzing |
| 093–095 | Capstone | LRU cache, concurrent URL fetcher, CLI with flags+JSON |

Deliberate gotchas: slice aliasing, nil-map writes, nil-interface-not-nil,
loop-variable capture, ignored `err`, `defer` in loops, unclosed channel
`range`, lost updates without a Mutex (also try `go test -race` there).

## Maintainers

```sh
make verify   # every solution passes AND every exercise fails
make test     # go test across solutions/
```

`--verify-solutions` fails if any solution breaks or any exercise
accidentally passes. Keep each fix small and each hint answer-free.
