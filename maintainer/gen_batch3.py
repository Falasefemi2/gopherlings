"""Batch 3: errors, generics, concurrency (056-081)."""
import sys
sys.path.insert(0, ".")
from genlib import add_manifest, write_files

def ex(edir, topic, mode, hint, ex_files, sol_files, test_files=None, expected=None):
    num = edir.split("_")[0]
    add_manifest(num, edir, mode, hint, topic, expected)
    write_files(edir, {"ex": ex_files, "sol": sol_files, "test": test_files})

# ---- errors ----
ex("056_error_values", "errors", "test",
   "What does a nil error mean? What should Fail return on success?",
   {"main.go": """// 056: error is a value: nil means success. Check errors with
// `if err != nil`, and create them with errors.New / fmt.Errorf.
// TODO: return nil on the happy path.
package main

import "errors"

func Fail(bad bool) error {
\tif bad {
\t\treturn errors.New("bad")
\t}
\treturn errors.New("ok")
}
"""},
   {"main.go": """// 056: error is a value: nil means success. Check errors with
// `if err != nil`, and create them with errors.New / fmt.Errorf.
package main

import "errors"

func Fail(bad bool) error {
\tif bad {
\t\treturn errors.New("bad")
\t}
\treturn nil
}
"""},
   {"exercise_test.go": """package main

import "testing"

func TestFail(t *testing.T) {
\tif Fail(false) != nil {
\t\tt.Fatal("success should be nil")
\t}
\tif Fail(true) == nil {
\t\tt.Fatal("failure should be non-nil")
\t}
}
"""})

ex("057_wrap_w", "errors", "test",
   "Which verb preserves the chain for errors.Is/As?",
   {"main.go": """// 057: Wrap with fmt.Errorf("...: %w", err) to keep the chain.
// %v formats but breaks Is/As. Add context at each layer.
// TODO: wrap so errors.Is still finds the sentinel.
package main

import (
\t"errors"
\t"fmt"
)

var ErrBase = errors.New("base")

func Middle() error {
\treturn fmt.Errorf("middle: %v", ErrBase)
}
"""},
   {"main.go": """// 057: Wrap with fmt.Errorf("...: %w", err) to keep the chain.
// %v formats but breaks Is/As. Add context at each layer.
package main

import (
\t"errors"
\t"fmt"
)

var ErrBase = errors.New("base")

func Middle() error {
\treturn fmt.Errorf("middle: %w", ErrBase)
}
"""},
   {"exercise_test.go": """package main

import (
\t"errors"
\t"testing"
)

func TestWrap(t *testing.T) {
\tif !errors.Is(Middle(), ErrBase) {
\t\tt.Fatalf("chain broken: %v", Middle())
\t}
}
"""})

ex("058_errors_is", "errors", "test",
   "Should you compare errors with == when they may be wrapped?",
   {"main.go": """// 058: errors.Is walks the wrap chain. == only matches the exact
// value, so wrapped sentinels need Is.
// TODO: detect ErrGone even when wrapped.
package main

import (
\t"errors"
\t"fmt"
)

var ErrGone = errors.New("gone")

func Gone() error { return fmt.Errorf("op: %w", ErrGone) }

func IsGone(err error) bool { return err == ErrGone }
"""},
   {"main.go": """// 058: errors.Is walks the wrap chain. == only matches the exact
// value, so wrapped sentinels need Is.
package main

import (
\t"errors"
\t"fmt"
)

var ErrGone = errors.New("gone")

func Gone() error { return fmt.Errorf("op: %w", ErrGone) }

func IsGone(err error) bool { return errors.Is(err, ErrGone) }
"""},
   {"exercise_test.go": """package main

import "testing"

func TestIsGone(t *testing.T) {
\tif !IsGone(Gone()) {
\t\tt.Fatal("should detect wrapped ErrGone")
\t}
\tif IsGone(nil) {
\t\tt.Fatal("nil is not gone")
\t}
}
"""})

ex("059_errors_as", "errors", "test",
   "How do you extract a *TypedError from a wrapped chain?",
   {"main.go": """// 059: errors.As finds the first error of a target type in the
// chain. Use it for structured errors with extra fields.
// TODO: extract *FieldError and report its Field.
package main

import (
\t"fmt"
)

type FieldError struct {
\tField string
\tMsg   string
}

func (e *FieldError) Error() string { return e.Field + ": " + e.Msg }

func Bad() error { return fmt.Errorf("req: %w", &FieldError{Field: "age", Msg: "neg"}) }

func FieldOf(err error) string {
\tif err == nil {
\t\treturn ""
\t}
\treturn "?"
}
"""},
   {"main.go": """// 059: errors.As finds the first error of a target type in the
// chain. Use it for structured errors with extra fields.
package main

import (
\t"errors"
\t"fmt"
)

type FieldError struct {
\tField string
\tMsg   string
}

func (e *FieldError) Error() string { return e.Field + ": " + e.Msg }

func Bad() error { return fmt.Errorf("req: %w", &FieldError{Field: "age", Msg: "neg"}) }

func FieldOf(err error) string {
\tvar fe *FieldError
\tif errors.As(err, &fe) {
\t\treturn fe.Field
\t}
\treturn ""
}
"""},
   {"exercise_test.go": """package main

import "testing"

func TestFieldOf(t *testing.T) {
\tif FieldOf(Bad()) != "age" {
\t\tt.Fatalf("got %q", FieldOf(Bad()))
\t}
\tif FieldOf(nil) != "" {
\t\tt.Fatal("nil has no field")
\t}
}
"""})

ex("060_errors_join", "errors", "test",
   "How do you combine several errors and still match each one?",
   {"main.go": """// 060: errors.Join (Go 1.20+) merges errors; Is/As match any part.
// Useful for validation collecting every problem at once.
// TODO: join both errors so Is finds each.
package main

import "errors"

var (
\tErrA = errors.New("a")
\tErrB = errors.New("b")
)

func Both() error {
\treturn errors.Join()
}
"""},
   {"main.go": """// 060: errors.Join (Go 1.20+) merges errors; Is/As match any part.
// Useful for validation collecting every problem at once.
package main

import "errors"

var (
\tErrA = errors.New("a")
\tErrB = errors.New("b")
)

func Both() error {
\treturn errors.Join(ErrA, ErrB)
}
"""},
   {"exercise_test.go": """package main

import (
\t"errors"
\t"testing"
)

func TestBoth(t *testing.T) {
\terr := Both()
\tif !errors.Is(err, ErrA) || !errors.Is(err, ErrB) {
\t\tt.Fatalf("joined error should match both, got %v", err)
\t}
}
"""})
# broken errors.Join() with no args returns nil -> Is fails. Good.

ex("061_panic_recover", "errors", "test",
   "Where must recover run to catch a panic? What should Safe return?",
   {"main.go": """// 061: panic is for the truly unrecoverable. recover only works
// in a deferred func; libraries should return errors instead.
// TODO: recover and report the panic as an error.
package main

import "fmt"

func Safe(f func()) (err error) {
\tf()
\treturn nil
}

func Boom2() { panic("bang") }

var _ = fmt.Sprint
"""},
   {"main.go": """// 061: panic is for the truly unrecoverable. recover only works
// in a deferred func; libraries should return errors instead.
package main

import "fmt"

func Safe(f func()) (err error) {
\tdefer func() {
\t\tif r := recover(); r != nil {
\t\t\terr = fmt.Errorf("panic: %v", r)
\t\t}
\t}()
\tf()
\treturn nil
}

func Boom2() { panic("bang") }
"""},
   {"exercise_test.go": """package main

import "testing"

func TestSafe(t *testing.T) {
\tif err := Safe(Boom2); err == nil {
\t\tt.Fatal("expected panic converted to error")
\t}
\tif err := Safe(func() {}); err != nil {
\t\tt.Fatalf("no panic should be nil, got %v", err)
\t}
}
"""})
# broken: Safe(Boom2) panics -> test panics -> fail. Good.

ex("062_sentinel_typed", "errors", "test",
   "When is a plain sentinel enough, and when do you need As?",
   {"main.go": """// 062: Sentinels (var ErrX) suit fixed cases; typed errors suit
// dynamic context. Callers use Is for the first, As for the second.
// TODO: return the sentinel for "missing", typed error otherwise.
package main

import "errors"

var ErrMissing = errors.New("missing")

type BadValue struct{ V string }

func (e *BadValue) Error() string { return "bad:" + e.V }

func Classify(v string) error {
\tif v == "" {
\t\treturn &BadValue{V: v}
\t}
\treturn ErrMissing
}
"""},
   {"main.go": """// 062: Sentinels (var ErrX) suit fixed cases; typed errors suit
// dynamic context. Callers use Is for the first, As for the second.
package main

import "errors"

var ErrMissing = errors.New("missing")

type BadValue struct{ V string }

func (e *BadValue) Error() string { return "bad:" + e.V }

func Classify(v string) error {
\tif v == "" {
\t\treturn ErrMissing
\t}
\treturn &BadValue{V: v}
}
"""},
   {"exercise_test.go": """package main

import (
\t"errors"
\t"testing"
)

func TestClassify(t *testing.T) {
\tif !errors.Is(Classify(""), ErrMissing) {
\t\tt.Fatal("empty should be ErrMissing")
\t}
\tvar bv *BadValue
\tif !errors.As(Classify("zzz"), &bv) {
\t\tt.Fatal("other should be *BadValue")
\t}
}
"""})
# broken: Classify("") returns &BadValue{V:""} -> Is(ErrMissing) false -> fail. Good.

# ---- generics ----
ex("063_generic_func", "generics", "test",
   "Where do type parameters go? What does the body work for?",
   {"main.go": """// 063: Type parameters list after the name: func First[T any](s []T) T.
// The same code works for every element type.
// TODO: return the first element (zero value when empty).
package main

func First2[T any](s []T) T {
\tvar zero T
\t_ = zero
\tpanic("todo")
}
"""},
   {"main.go": """// 063: Type parameters list after the name: func First[T any](s []T) T.
// The same code works for every element type.
package main

func First2[T any](s []T) T {
\tif len(s) == 0 {
\t\tvar zero T
\t\treturn zero
\t}
\treturn s[0]
}
"""},
   {"exercise_test.go": """package main

import "testing"

func TestFirst2(t *testing.T) {
\tif First2([]int{7, 8}) != 7 {
\t\tt.Fatal("int failed")
\t}
\tif First2([]string{"a"}) != "a" {
\t\tt.Fatal("string failed")
\t}
\tif First2[int](nil) != 0 {
\t\tt.Fatal("empty should be zero")
\t}
}
"""})
# broken panics -> fail. Good.

ex("064_comparable", "generics", "test",
   "Which constraint allows == on values of type T?",
   {"main.go": """// 064: comparable constrains to types supporting ==/!=, so maps
// and dedup can use it. any does not allow ==.
// TODO: constrain T so == compiles.
package main

func Has[T any](s []T, v T) bool {
\tfor _, x := range s {
\t\tif x == v {
\t\t\treturn true
\t\t}
\t}
\treturn false
}
"""},
   {"main.go": """// 064: comparable constrains to types supporting ==/!=, so maps
// and dedup can use it. any does not allow ==.
package main

func Has[T comparable](s []T, v T) bool {
\tfor _, x := range s {
\t\tif x == v {
\t\t\treturn true
\t\t}
\t}
\treturn false
}
"""},
   {"exercise_test.go": """package main

import "testing"

func TestHas(t *testing.T) {
\tif !Has([]string{"a", "b"}, "b") {
\t\tt.Fatal("should find b")
\t}
\tif Has([]int{1}, 2) {
\t\tt.Fatal("should not find 2")
\t}
}
"""})
# broken: `x == v` with T any -> compile error. Good fail.

ex("065_ordered", "generics", "test",
   "Which stdlib constraint allows < on type T?",
   {"main.go": """// 065: cmp.Ordered covers ints, floats and strings for <,>.
// Import "cmp"; constraints live in signatures, not bodies.
// TODO: return the smaller of a and b.
package main

func Min2[T cmp.Ordered](a, b T) T {
\tif a < b {
\t\treturn a
\t}
\treturn b
}
"""},
   {"main.go": """// 065: cmp.Ordered covers ints, floats and strings for <,>.
// Import "cmp"; constraints live in signatures, not bodies.
package main

import "cmp"

func Min2[T cmp.Ordered](a, b T) T {
\tif a < b {
\t\treturn a
\t}
\treturn b
}
"""},
   {"exercise_test.go": """package main

import "testing"

func TestMin2(t *testing.T) {
\tif Min2(2, 1) != 1 {
\t\tt.Fatal("int min failed")
\t}
\tif Min2("b", "a") != "a" {
\t\tt.Fatal("string min failed")
\t}
}
"""})
# broken uses cmp.Ordered without importing cmp -> compile error. Good.

ex("066_generic_stack", "generics", "test",
   "How does a generic type declare its parameter?",
   {"main.go": """// 066: Generic types take parameters too: type Stack[T any].
// Methods use the same T; zero value of T is the default.
// TODO: Push/Pop in LIFO order.
package main

type Stack[T any] struct{ items []T }

func (s *Stack[T]) Push(v T) { s.items = append(s.items, v) }

func (s *Stack[T]) Pop() (T, bool) {
\tvar zero T
\tif len(s.items) == 0 {
\t\treturn zero, false
\t}
\tv := s.items[0]
\ts.items = s.items[1:]
\treturn v, true
}
"""},
   {"main.go": """// 066: Generic types take parameters too: type Stack[T any].
// Methods use the same T; zero value of T is the default.
package main

type Stack[T any] struct{ items []T }

func (s *Stack[T]) Push(v T) { s.items = append(s.items, v) }

func (s *Stack[T]) Pop() (T, bool) {
\tvar zero T
\tif len(s.items) == 0 {
\t\treturn zero, false
\t}
\tv := s.items[len(s.items)-1]
\ts.items = s.items[:len(s.items)-1]
\treturn v, true
}
"""},
   {"exercise_test.go": """package main

import "testing"

func TestStack(t *testing.T) {
\tvar s Stack[int]
\ts.Push(1)
\ts.Push(2)
\tif v, _ := s.Pop(); v != 2 {
\t\tt.Fatalf("got %d want 2 (LIFO)", v)
\t}
\tif v, _ := s.Pop(); v != 1 {
\t\tt.Fatalf("got %d want 1", v)
\t}
}
"""})
# broken is FIFO -> first Pop returns 1, want 2 -> fail. Good.

ex("067_no_generics", "generics", "test",
   "Could a plain interface or concrete type do here?",
   {"main.go": """// 067: Reach for generics only when one implementation truly
// fits many types. Dumping to strings needs only fmt/Stringer.
// TODO: describe any value without generics.
package main

import "fmt"

func DescribeAny[T any](v T) string {
\treturn fmt.Sprint(v)
}
"""},
   {"main.go": """// 067: Reach for generics only when one implementation truly
// fits many types. Dumping to strings needs only fmt/Stringer.
package main

import "fmt"

func DescribeAny(v any) string {
\treturn fmt.Sprintf("%v (%T)", v, v)
}
"""},
   {"exercise_test.go": """package main

import "testing"

func TestDescribeAny(t *testing.T) {
\tif DescribeAny(42) != "42 (int)" {
\t\tt.Fatalf("got %q", DescribeAny(42))
\t}
}
"""})
# broken generic version: DescribeAny(42) with T inferred -> same output "42 (int)" -> PASSES! Bad. Need broken to fail: make broken format wrong: `return fmt.Sprint(v)` -> "42" != "42 (int)" fails. Fixed adds type. Let's change broken body.

# ---- concurrency ----
ex("068_goroutines", "concurrency", "test",
   "How do you wait for goroutines to finish before returning?",
   {"main.go": """// 068: `go f()` runs f concurrently. The caller must wait,
// or results vanish when the function returns. Channels/WaitGroup sync.
// TODO: compute the sum concurrently and wait for it.
package main

func SumAsync(xs []int) int {
\tsum := 0
\tgo func() {
\t\tfor _, x := range xs {
\t\t\tsum += x
\t\t}
\t}()
\treturn sum
}
"""},
   {"main.go": """// 068: `go f()` runs f concurrently. The caller must wait,
// or results vanish when the function returns. Channels/WaitGroup sync.
package main

func SumAsync(xs []int) int {
\tdone := make(chan int, 1)
\tgo func() {
\t\tsum := 0
\t\tfor _, x := range xs {
\t\t\tsum += x
\t\t}
\t\tdone <- sum
\t}()
\treturn <-done
}
"""},
   {"exercise_test.go": """package main

import "testing"

func TestSumAsync(t *testing.T) {
\tif SumAsync([]int{1, 2, 3, 4}) != 10 {
\t\tt.Fatalf("got %d", SumAsync([]int{1, 2, 3, 4}))
\t}
}
"""})
# broken returns 0 (race, goroutine hasn't run) -> usually fails. Flaky? sum could be partial but almost always 0 since return runs before goroutine. Deterministic enough? Goroutine scheduling: `go func` then immediate return; scheduler *could* run goroutine first? In practice return happens first, sum=0. There's a data race but test reads sum without sync - race detector would flag, but value almost always 0. Accept.

ex("069_channels", "concurrency", "test",
   "Who sends, who receives, and who should close?",
   {"main.go": """// 069: Channels move values between goroutines. Senders usually
// close when done; receivers range until close.
// TODO: send 1..3 then close so the range ends.
package main

func Produce() []int {
\tch := make(chan int)
\tgo func() {
\t\tfor i := 1; i <= 3; i++ {
\t\t\tch <- i
\t\t}
\t}()
\tvar out []int
\tfor v := range ch {
\t\tout = append(out, v)
\t}
\treturn out
}
"""},
   {"main.go": """// 069: Channels move values between goroutines. Senders usually
// close when done; receivers range until close.
package main

func Produce() []int {
\tch := make(chan int)
\tgo func() {
\t\tfor i := 1; i <= 3; i++ {
\t\t\tch <- i
\t\t}
\t\tclose(ch)
\t}()
\tvar out []int
\tfor v := range ch {
\t\tout = append(out, v)
\t}
\treturn out
}
"""},
   {"exercise_test.go": """package main

import (
\t"reflect"
\t"testing"
\t"time"
)

func TestProduce(t *testing.T) {
\tdone := make(chan []int, 1)
\tgo func() { done <- Produce() }()
\tselect {
\tcase got := <-done:
\t\tif !reflect.DeepEqual(got, []int{1, 2, 3}) {
\t\t\tt.Fatalf("got %v", got)
\t\t}
\tcase <-time.After(500 * time.Millisecond):
\t\tt.Fatal("deadlock: channel never closed, range never ends")
\t}
}
"""})
# broken deadlocks -> test timeout fails after 2s. Good but slows verify by 2s for the failing case. Acceptable (verify expects exercise to fail; 2s wait). Could reduce to 300ms. Let's keep 500ms? Already 2s. Change to 500ms to speed verify.

ex("070_buffered", "concurrency", "test",
   "When does a send block? What does capacity change?",
   {"main.go": """// 070: Unbuffered sends block until a receiver arrives. Buffered
// sends (make(chan T, n)) block only when the buffer is full.
// TODO: make the two sends succeed with no receiver yet.
package main

func TwoSends() int {
\tch := make(chan int)
\tch <- 1
\tch <- 2
\treturn len(ch)
}
"""},
   {"main.go": """// 070: Unbuffered sends block until a receiver arrives. Buffered
// sends (make(chan T, n)) block only when the buffer is full.
package main

func TwoSends() int {
\tch := make(chan int, 2)
\tch <- 1
\tch <- 2
\treturn len(ch)
}
"""},
   {"exercise_test.go": """package main

import (
\t"testing"
\t"time"
)

func TestTwoSends(t *testing.T) {
\tdone := make(chan int, 1)
\tgo func() { done <- TwoSends() }()
\tselect {
\tcase n := <-done:
\t\tif n != 2 {
\t\t\tt.Fatalf("got %d want 2", n)
\t\t}
\tcase <-time.After(500 * time.Millisecond):
\t\tt.Fatal("blocked: unbuffered channel needs a receiver")
\t}
}
"""})
# broken blocks forever on first send -> timeout fail. Good.

ex("071_select", "concurrency", "test",
   "How do you wait on several channels at once, with a timeout?",
   {"main.go": """// 071: select waits on many channels; first ready wins. Combine
// with time.After for timeouts, default for non-blocking.
// TODO: return "fast" or "slow" depending on which answers first.
package main

import "time"

func Race(fast, slow <-chan string) string {
\ttime.Sleep(5 * time.Millisecond)
\treturn <-slow
}
"""},
   {"main.go": """// 071: select waits on many channels; first ready wins. Combine
// with time.After for timeouts, default for non-blocking.
package main

import "time"

func Race(fast, slow <-chan string) string {
\tselect {
\tcase s := <-fast:
\t\treturn s
\tcase s := <-slow:
\t\treturn s
\tcase <-time.After(2 * time.Second):
\t\treturn "timeout"
\t}
}
"""},
   {"exercise_test.go": """package main

import "testing"

func TestRace(t *testing.T) {
\tfast := make(chan string, 1)
\tslow := make(chan string, 1)
\tfast <- "fast"
\tslow <- "slow"
\tif Race(fast, slow) != "fast" {
\t\tt.Fatal("fast channel should win")
\t}
}
"""})
# broken sleeps then reads slow -> returns "slow" -> fail. Good. But if slow empty? Test buffers both, so <-slow succeeds returning "slow". Good.

ex("072_waitgroup", "concurrency", "test",
   "When do you Add, Done and Wait? What happens if Add is late?",
   {"main.go": """// 072: sync.WaitGroup waits for a set of goroutines. Add before
// starting them, Done when each ends (often deferred), Wait at the end.
// TODO: wait for all 10 increments.
package main

import "sync"

func Count10() int {
\tvar mu sync.Mutex
\tn := 0
\tfor i := 0; i < 10; i++ {
\t\tgo func() {
\t\t\tmu.Lock()
\t\t\tn++
\t\t\tmu.Unlock()
\t\t}()
\t}
\treturn n
}
"""},
   {"main.go": """// 072: sync.WaitGroup waits for a set of goroutines. Add before
// starting them, Done when each ends (often deferred), Wait at the end.
package main

import "sync"

func Count10() int {
\tvar mu sync.Mutex
\tn := 0
\tvar wg sync.WaitGroup
\tfor i := 0; i < 10; i++ {
\t\twg.Add(1)
\t\tgo func() {
\t\t\tdefer wg.Done()
\t\t\tmu.Lock()
\t\t\tn++
\t\t\tmu.Unlock()
\t\t}()
\t}
\twg.Wait()
\treturn n
}
"""},
   {"exercise_test.go": """package main

import "testing"

func TestCount10(t *testing.T) {
\tfor i := 0; i < 20; i++ {
\t\tif Count10() != 10 {
\t\t\tt.Fatalf("got %d want 10", Count10())
\t\t}
\t}
}
"""})
# broken: no Add/Wait, returns n immediately (usually 0, race) -> fails. Also data race on n+return. Usually 0. Good. But flaky loop of 20 may occasionally pass once? Count10 broken returns n read immediately after launching goroutines; almost always 0. Even if scheduler runs some, !=10. The `t.Fatalf` calls Count10() again (double call) - prints second call's value, fine.
# Note: broken imports sync but only uses sync.Mutex -> used, ok compiles.

ex("073_mutex", "concurrency", "test",
   "What happens when many goroutines touch one variable?",
   {"main.go": """// 073: sync.Mutex serializes access. Lock/Unlock around the shared
// section; run `go test -race` to prove the race is gone.
// TODO: guard the counter so the total is exact.
package main

import "sync"

func Total(n int) int {
\tvar wg sync.WaitGroup
\tcount := 0
\tfor i := 0; i < n; i++ {
\t\twg.Add(1)
\t\tgo func() {
\t\t\tdefer wg.Done()
\t\t\tcount++
\t\t}()
\t}
\twg.Wait()
\treturn count
}
"""},
   {"main.go": """// 073: sync.Mutex serializes access. Lock/Unlock around the shared
// section; run `go test -race` to prove the race is gone.
package main

import "sync"

func Total(n int) int {
\tvar wg sync.WaitGroup
\tvar mu sync.Mutex
\tcount := 0
\tfor i := 0; i < n; i++ {
\t\twg.Add(1)
\t\tgo func() {
\t\t\tdefer wg.Done()
\t\t\tmu.Lock()
\t\t\tcount++
\t\t\tmu.Unlock()
\t\t}()
\t}
\twg.Wait()
\treturn count
}
"""},
   {"exercise_test.go": """package main

import "testing"

func TestTotal(t *testing.T) {
\tif Total(2000) != 2000 {
\t\tt.Fatalf("got %d want 2000 (lost updates without a mutex?)", Total(2000))
\t}
}
"""})
# broken loses updates -> almost certainly < 2000. Small flake chance of exactly 2000? Practically zero with 2000 goroutines.

ex("074_atomic", "concurrency", "test",
   "When is atomic enough instead of a mutex?",
   {"main.go": """// 074: sync/atomic gives lock-free counters/flags. Use for a single
// integer; reach for Mutex for compound state.
// TODO: increment atomically.
package main

import "sync/atomic"

func AtomicTotal(n int) int64 {
\tvar c int64
\tdone := make(chan struct{}, n)
\tfor i := 0; i < n; i++ {
\t\tgo func() {
\t\t\tc++
\t\t\tdone <- struct{}{}
\t\t}()
\t}
\tfor i := 0; i < n; i++ {
\t\t<-done
\t}
\treturn atomic.LoadInt64(&c)
}
"""},
   {"main.go": """// 074: sync/atomic gives lock-free counters/flags. Use for a single
// integer; reach for Mutex for compound state.
package main

import "sync/atomic"

func AtomicTotal(n int) int64 {
\tvar c int64
\tdone := make(chan struct{}, n)
\tfor i := 0; i < n; i++ {
\t\tgo func() {
\t\t\tatomic.AddInt64(&c, 1)
\t\t\tdone <- struct{}{}
\t\t}()
\t}
\tfor i := 0; i < n; i++ {
\t\t<-done
\t}
\treturn atomic.LoadInt64(&c)
}
"""},
   {"exercise_test.go": """package main

import "testing"

func TestAtomicTotal(t *testing.T) {
\tif AtomicTotal(2000) != 2000 {
\t\tt.Fatalf("got %d", AtomicTotal(2000))
\t}
}
"""})
# broken c++ racy -> usually < 2000. Good.

ex("075_ctx_cancel", "concurrency", "test",
   "How does a goroutine learn its work was cancelled?",
   {"main.go": """// 075: context.Context carries cancellation. Parents cancel via
// cancel(); workers watch <-ctx.Done() and stop.
// TODO: stop early when ctx is cancelled.
package main

import (
\t"context"
\t"time"
)

func Work(ctx context.Context) string {
\ttime.Sleep(50 * time.Millisecond)
\treturn "done"
}
"""},
   {"main.go": """// 075: context.Context carries cancellation. Parents cancel via
// cancel(); workers watch <-ctx.Done() and stop.
package main

import (
\t"context"
\t"time"
)

func Work(ctx context.Context) string {
\tselect {
\tcase <-time.After(50 * time.Millisecond):
\t\treturn "done"
\tcase <-ctx.Done():
\t\treturn "cancelled:" + ctx.Err().Error()
\t}
}
"""},
   {"exercise_test.go": """package main

import (
\t"context"
\t"strings"
\t"testing"
\t"time"
)

func TestWork(t *testing.T) {
\tctx, cancel := context.WithCancel(context.Background())
\tcancel()
\tif got := Work(ctx); !strings.HasPrefix(got, "cancelled") {
\t\tt.Fatalf("got %q", got)
\t}
\tif got := Work(context.Background()); got != "done" {
\t\tt.Fatalf("got %q", got)
\t}
\t_ = time.Now
}
"""})
# broken returns "cancelled" without suffix: HasPrefix("cancelled") passes! Bad. Fix: broken must fail: make broken ignore ctx entirely: `time.Sleep(50ms); return "done"`? Then cancelled case returns "done" -> fail. Rewrite broken to not select on ctx.

ex("076_ctx_timeout", "concurrency", "test",
   "How do you bound how long an operation may take?",
   {"main.go": """// 076: context.WithTimeout auto-cancels after a deadline. The callee
// sees ctx.Done(); the caller checks ctx.Err() == context.DeadlineExceeded.
// TODO: time out the slow operation.
package main

import (
\t"context"
\t"time"
)

func Fetch(ctx context.Context) error {
\ttime.Sleep(200 * time.Millisecond)
\treturn nil
}
"""},
   {"main.go": """// 076: context.WithTimeout auto-cancels after a deadline. The callee
// sees ctx.Done(); the caller checks ctx.Err() == context.DeadlineExceeded.
package main

import (
\t"context"
\t"time"
)

func Fetch(ctx context.Context) error {
\tselect {
\tcase <-time.After(200 * time.Millisecond):
\t\treturn nil
\tcase <-ctx.Done():
\t\treturn ctx.Err()
\t}
}
"""},
   {"exercise_test.go": """package main

import (
\t"context"
\t"testing"
\t"time"
)

func TestFetchTimeout(t *testing.T) {
\tctx, cancel := context.WithTimeout(context.Background(), 20*time.Millisecond)
\tdefer cancel()
\tif err := Fetch(ctx); err != context.DeadlineExceeded {
\t\tt.Fatalf("got %v", err)
\t}
}
"""})
# broken == fixed! Both select on ctx -> passes. Need broken to fail: broken ignores ctx: `time.Sleep(200ms); return nil` -> test gets nil != DeadlineExceeded -> fail. Fix broken.

ex("077_worker_pool", "concurrency", "test",
   "How do N workers share one jobs channel and report results?",
   {"main.go": """// 077: A worker pool fans jobs to N goroutines via a channel and
// collects results. Close jobs when done; workers range until close.
// TODO: run 3 workers so every job is doubled.
package main

import "sync"

func Pool(jobs []int) []int {
\ttype task struct {
\t\ti, v int
\t}
\tjc := make(chan task)
\tres := make([]int, len(jobs))
\tvar wg sync.WaitGroup
\tfor w := 0; w < 3; w++ {
\t\twg.Add(1)
\t\tgo func() {
\t\t\tdefer wg.Done()
\t\t\tfor t := range jc {
\t\t\t\tres[t.i] = t.v
\t\t\t}
\t\t}()
\t}
\tfor i, v := range jobs {
\t\tjc <- task{i, v}
\t}
\tclose(jc)
\twg.Wait()
\treturn res
}
"""},
   {"main.go": """// 077: A worker pool fans jobs to N goroutines via a channel and
// collects results. Close jobs when done; workers range until close.
package main

import "sync"

func Pool(jobs []int) []int {
\ttype task struct {
\t\ti, v int
\t}
\tjc := make(chan task)
\tres := make([]int, len(jobs))
\tvar wg sync.WaitGroup
\tfor w := 0; w < 3; w++ {
\t\twg.Add(1)
\t\tgo func() {
\t\t\tdefer wg.Done()
\t\t\tfor t := range jc {
\t\t\t\tres[t.i] = t.v * 2
\t\t\t}
\t\t}()
\t}
\tfor i, v := range jobs {
\t\tjc <- task{i, v}
\t}
\tclose(jc)
\twg.Wait()
\treturn res
}
"""},
   {"exercise_test.go": """package main

import (
\t"reflect"
\t"sort"
\t"testing"
)

func TestPool(t *testing.T) {
\tgot := Pool([]int{1, 2, 3, 4, 5})
\tsort.Ints(got)
\tif !reflect.DeepEqual(got, []int{2, 4, 6, 8, 10}) {
\t\tt.Fatalf("got %v", got)
\t}
}
"""})
# broken is sequential doubling -> PASSES (same result)! Bad. Need broken to actually use pool skeleton but with bug: e.g., forgets to close/wait? Must fail. Make broken: single worker but forgets close -> deadlock? Test would hang. Better: broken launches workers but never sends? Returns zeros -> fail. Let's make broken: workers range jc but main never closes -> deadlock... test hangs.
# Alternative: broken uses pool but writes res[t.i] = t.v (forgot *2) -> fails values. And comment says TODO double. Sequential vs pool indistinguishable by test, so make the "bug" the missing *2. Rewrite broken pool with missing *2? But then it doesn't teach pool structure... Simpler: broken code below is sequential but returns j+1? No.
# Let's make broken a pool with 3 workers that forgets wg.Wait (returns early, usually zeros). Flaky but usually fails. Hmm.
# Deterministic: broken pool writes `res[t.i] = t.v` (no doubling) -> always fails. Fixed doubles. The pool structure is present in both; the fix is small. Accept: learner's "fix" is the *2, but they also see pool structure. Slightly weak but fine. Actually better: broken forgets `close(jc)` AND uses non-blocking? No.
# Decision: broken = pool skeleton with `res[t.i] = t.v` (missing *2) -> deterministic fail.

ex("078_fan_in", "concurrency", "test",
   "How do you merge two channels into one?",
   {"main.go": """// 078: Fan-in merges many channels into one. Launch one goroutine
// per input, forward until inputs close, then close the output.
// TODO: merge a and b into a single channel.
package main

func FanIn(a, b <-chan int) <-chan int {
\tout := make(chan int)
\tgo func() {
\t\tfor v := range a {
\t\t\tout <- v
\t\t}
\t\tclose(out)
\t}()
\treturn out
}
"""},
   {"main.go": """// 078: Fan-in merges many channels into one. Launch one goroutine
// per input, forward until inputs close, then close the output.
package main

import "sync"

func FanIn(a, b <-chan int) <-chan int {
\tout := make(chan int)
\tvar wg sync.WaitGroup
\twg.Add(2)
\tgo func() { defer wg.Done(); for v := range a { out <- v } }()
\tgo func() { defer wg.Done(); for v := range b { out <- v } }()
\tgo func() { wg.Wait(); close(out) }()
\treturn out
}
"""},
   {"exercise_test.go": """package main

import (
\t"sort"
\t"testing"
)

func TestFanIn(t *testing.T) {
\ta := make(chan int, 2)
\tb := make(chan int, 2)
\ta <- 1
\ta <- 3
\tclose(a)
\tb <- 2
\tclose(b)
\tvar got []int
\tfor v := range FanIn(a, b) {
\t\tgot = append(got, v)
\t}
\tsort.Ints(got)
\tif len(got) != 3 || got[0] != 1 || got[1] != 2 || got[2] != 3 {
\t\tt.Fatalf("got %v", got)
\t}
}
"""})
# broken == fixed! Need broken to fail: e.g., only forwards a, ignores b -> got [1,3] len2 -> fail. Fix broken to forward only a.

ex("079_loop_capture", "concurrency", "test",
   "Which variable does each closure share here?",
   {"main.go": """// 079: GOTCHA: closures share the variables they capture. (Go 1.22
// made loop vars per-iteration, but an outer variable is still shared.)
// Here i lives OUTSIDE the loop, so every func sees the final value.
// TODO: capture each iteration's value.
package main

func Closures() []int {
\tvar fns []func() int
\ti := 0
\tfor ; i < 3; i++ {
\t\tfns = append(fns, func() int { return i })
\t}
\tout := []int{fns[0](), fns[1](), fns[2]()}
\treturn out
}
"""},
   {"main.go": """// 079: GOTCHA: closures share the variables they capture. (Go 1.22
// made loop vars per-iteration, but an outer variable is still shared.)
// Pass the value as a parameter to capture it.
package main

func Closures() []int {
\tvar fns []func() int
\ti := 0
\tfor ; i < 3; i++ {
\t\tfns = append(fns, func(v int) func() int {
\t\t\treturn func() int { return v }
\t\t}(i))
\t}
\tout := []int{fns[0](), fns[1](), fns[2]()}
\treturn out
}
"""},
   {"exercise_test.go": """package main

import (
\t"reflect"
\t"testing"
)

func TestClosures(t *testing.T) {
\tif got := Closures(); !reflect.DeepEqual(got, []int{0, 1, 2}) {
\t\tt.Fatalf("got %v want [0 1 2]", got)
\t}
}
"""})
# broken returns [3,3,3] -> fail. Fixed [0,1,2]. Good.

ex("080_errgroup_hand", "concurrency", "test",
   "How do you collect the first error from many goroutines?",
   {"main.go": """// 080: errgroup pattern by hand: one goroutine per task, a buffered
// error channel (or mutex), Wait for all, return the first error.
// TODO: return the first non-nil error (if any).
package main

import "sync"

func RunAll(fs []func() error) error {
\tvar wg sync.WaitGroup
\tfor _, f := range fs {
\t\twg.Add(1)
\t\tgo func() {
\t\t\tdefer wg.Done()
\t\t\t_ = f()
\t\t}()
\t}
\twg.Wait()
\treturn nil
}
"""},
   {"main.go": """// 080: errgroup pattern by hand: one goroutine per task, a buffered
// error channel (or mutex), Wait for all, return the first error.
package main

import "sync"

func RunAll(fs []func() error) error {
\tvar wg sync.WaitGroup
\terrs := make(chan error, len(fs))
\tfor _, f := range fs {
\t\twg.Add(1)
\t\tgo func() {
\t\t\tdefer wg.Done()
\t\t\tif err := f(); err != nil {
\t\t\t\terrs <- err
\t\t\t}
\t\t}()
\t}
\twg.Wait()
\tclose(errs)
\tfor err := range errs {
\t\treturn err
\t}
\treturn nil
}
"""},
   {"exercise_test.go": """package main

import (
\t"errors"
\t"testing"
)

func TestRunAll(t *testing.T) {
\tok := func() error { return nil }
\tbad := func() error { return errors.New("x") }
\tif err := RunAll([]func() error{ok, ok}); err != nil {
\t\tt.Fatalf("got %v", err)
\t}
\tif err := RunAll([]func() error{ok, bad}); err == nil {
\t\tt.Fatal("expected error")
\t}
}
"""})
# broken == fixed! Need broken to fail: classic bug: `for _, f := range fs { go func() { f() }() }` in pre-1.22 captures loop var f -> all goroutines run last f. In Go 1.22 per-iteration, no bug. To make deterministic fail in 1.22: use index bug: `for i := range fs { go func() { fs[i]() }() }` with i outer? Still per-iteration in 1.22. Hmm.
# Make broken ignore errors: `go func() { defer wg.Done(); f() }()` discards err -> RunAll([ok,bad]) returns nil -> fail. Fixed sends errs. Rewrite broken to discard.

ex("081_chan_range_close", "concurrency", "test",
   "Who closes the channel so `for range` can finish?",
   {"main.go": """// 081: GOTCHA: `for v := range ch` ends only when ch is closed.
// The sender closes when done; receivers must not double-close.
// TODO: close the channel after sending.
package main

func Sum3() int {
\tch := make(chan int)
\tgo func() {
\t\tch <- 1
\t\tch <- 2
\t\tch <- 3
\t}()
\tsum := 0
\tfor v := range ch {
\t\tsum += v
\t}
\treturn sum
}
"""},
   {"main.go": """// 081: GOTCHA: `for v := range ch` ends only when ch is closed.
// The sender closes when done; receivers must not double-close.
package main

func Sum3() int {
\tch := make(chan int)
\tgo func() {
\t\tch <- 1
\t\tch <- 2
\t\tch <- 3
\t\tclose(ch)
\t}()
\tsum := 0
\tfor v := range ch {
\t\tsum += v
\t}
\treturn sum
}
"""},
   {"exercise_test.go": """package main

import (
\t"testing"
\t"time"
)

func TestSum3(t *testing.T) {
\tdone := make(chan int, 1)
\tgo func() { done <- Sum3() }()
\tselect {
\tcase n := <-done:
\t\tif n != 6 {
\t\t\tt.Fatalf("got %d", n)
\t\t}
\tcase <-time.After(500 * time.Millisecond):
\t\tt.Fatal("deadlock: range never ends without close")
\t}
}
"""})

print("batch3 done")
