"""Batch 1: basics, control flow, functions (001-026)."""
import sys
sys.path.insert(0, ".")
from genlib import add_manifest, write_files
import pathlib
ROOT = pathlib.Path(".")

def ex(edir, topic, mode, hint, ex_files, sol_files, test_files=None, expected=None):
    num = edir.split("_")[0]
    add_manifest(num, edir, mode, hint, topic, expected)
    write_files(edir, {"ex": ex_files, "sol": sol_files, "test": test_files})

# 001 hello_world: missing import
ex("001_hello_world", "basics", "run",
   "Look at the top of the file. What package provides Println?",
   {"main.go": """// 001: Every Go program is made of packages. The entry point is
// package main with func main. Printing needs the "fmt" package.
// TODO: fix the compile error so the program prints the greeting.
package main

func main() {
\tfmt.Println("hello, gopher")
}
"""},
   {"main.go": """// 001: Every Go program is made of packages. The entry point is
// package main with func main. Printing needs the "fmt" package.
package main

import "fmt"

func main() {
\tfmt.Println("hello, gopher")
}
"""},
   expected="hello, gopher")

# 002 vars_var
ex("002_vars_var", "basics", "run",
   "What value does the variable hold when it is printed?",
   {"main.go": """// 002: var declares a variable with a type and an initial value.
// TODO: make the program print exactly: hello gopher
package main

import "fmt"

func main() {
\tvar name string = "world"
\tfmt.Println("hello " + name)
}
"""},
   {"main.go": """// 002: var declares a variable with a type and an initial value.
package main

import "fmt"

func main() {
\tvar name string = "gopher"
\tfmt.Println("hello " + name)
}
"""},
   expected="hello gopher")

# 003 short_declare
ex("003_short_declare", "basics", "run",
   "Read the compiler message: when is := allowed vs plain =?",
   {"main.go": """// 003: := declares AND assigns; a second := with no new variable
// on the left is a compile error. = assigns to an existing variable.
// TODO: fix the compile error so the program prints: b
package main

import "fmt"

func main() {
\tname := "a"
\tname := "b"
\tfmt.Println(name)
}
"""},
   {"main.go": """// 003: := declares AND assigns; a second := with no new variable
// on the left is a compile error. = assigns to an existing variable.
package main

import "fmt"

func main() {
\tname := "a"
\tname = "b"
\tfmt.Println(name)
}
"""},
   expected="b")

# 004 zero_values (test)
ex("004_zero_values", "basics", "test",
   "What are the zero values of int, string and bool?",
   {"main.go": """// 004: Every type has a zero value used when no value is given:
// 0 for numbers, "" for strings, false for bools, nil for the rest.
// TODO: return the zero values instead of these placeholders.
package main

func Zero() (int, string, bool) {
\treturn 1, "x", true
}
"""},
   {"main.go": """// 004: Every type has a zero value used when no value is given:
// 0 for numbers, "" for strings, false for bools, nil for the rest.
package main

func Zero() (int, string, bool) {
\treturn 0, "", false
}
"""},
   {"exercise_test.go": """package main

import "testing"

func TestZero(t *testing.T) {
\tn, s, b := Zero()
\tif n != 0 || s != "" || b != false {
\t\tt.Fatalf("got (%v,%q,%v), want (0,\\\"\\\",false)", n, s, b)
\t}
}
"""})

# 005 constants_iota
ex("005_constants_iota", "basics", "test",
   "How does iota count inside a const block?",
   {"main.go": """// 005: const values are fixed at compile time. iota counts
// 0,1,2... per line inside a const block. Great for enums.
// TODO: use iota so A=0, B=1, C=2.
package main

const (
\tA = 1
\tB = 2
\tC = 3
)
"""},
   {"main.go": """// 005: const values are fixed at compile time. iota counts
// 0,1,2... per line inside a const block. Great for enums.
package main

const (
\tA = iota
\tB
\tC
)
"""},
   {"exercise_test.go": """package main

import "testing"

func TestIota(t *testing.T) {
\tif A != 0 || B != 1 || C != 2 {
\t\tt.Fatalf("got A=%d B=%d C=%d, want 0 1 2", A, B, C)
\t}
}
"""})

# 006 unused_variable
ex("006_unused_variable", "basics", "run",
   "Go refuses to compile unused locals. Either use x or remove it.",
   {"main.go": """// 006: Go treats unused local variables as an error, not a warning.
// It keeps code honest. TODO: fix the compile error; print answer: 42
package main

import "fmt"

func main() {
\tx := 42
\tfmt.Println("answer: ...")
}
"""},
   {"main.go": """// 006: Go treats unused local variables as an error, not a warning.
// It keeps code honest.
package main

import "fmt"

func main() {
\tx := 42
\tfmt.Println("answer:", x)
}
"""},
   expected="answer: 42")

# 007 unused_import
ex("007_unused_import", "basics", "run",
   "Same rule for imports. Either use strings or drop the import.",
   {"main.go": """// 007: Unused imports are also a compile error. Your editor
// usually manages them, but understand why the compiler complains.
// TODO: fix the error so the program prints HELLO.
package main

import (
\t"fmt"
\t"strings"
)

func main() {
\tfmt.Println("hello")
}
"""},
   {"main.go": """// 007: Unused imports are also a compile error. Your editor
// usually manages them, but understand why the compiler complains.
package main

import (
\t"fmt"
\t"strings"
)

func main() {
\tfmt.Println(strings.ToUpper("hello"))
}
"""},
   expected="HELLO")

# 008 conversions
ex("008_conversions", "basics", "test",
   "What does string(65) produce? How do you convert a number to its decimal text?",
   {"main.go": """// 008: Go never converts implicitly. string(65) is "A" (rune),
// not "65". Use strconv for decimal text.
// TODO: return the decimal text of n.
package main

func Itoa(n int) string {
\treturn string(n)
}
"""},
   {"main.go": """// 008: Go never converts implicitly. string(65) is "A" (rune),
// not "65". Use strconv for decimal text.
package main

import "strconv"

func Itoa(n int) string {
\treturn strconv.Itoa(n)
}
"""},
   {"exercise_test.go": """package main

import "testing"

func TestItoa(t *testing.T) {
\tif got := Itoa(65); got != "65" {
\t\tt.Fatalf("got %q, want %q", got, "65")
\t}
\tif got := Itoa(-7); got != "-7" {
\t\tt.Fatalf("got %q, want %q", got, "-7")
\t}
}
"""})

# 009 fmt_verbs
ex("009_fmt_verbs", "basics", "run",
   "Which verb formats an int in decimal? Check what %s does to an int.",
   {"main.go": """// 009: fmt verbs are typed: %d for ints, %s for strings, %v for
// anything, %q for quoted strings. Wrong verbs show up in output.
// TODO: print exactly: answer: 42
package main

import "fmt"

func main() {
\tfmt.Printf("%s\\n", 42)
}
"""},
   {"main.go": """// 009: fmt verbs are typed: %d for ints, %s for strings, %v for
// anything, %q for quoted strings. Wrong verbs show up in output.
package main

import "fmt"

func main() {
\tfmt.Printf("%d\\n", 42)
}
"""},
   expected="answer: 42")

# 010 const_vs_var
ex("010_const_vs_var", "basics", "run",
   "Can a const be reassigned? What keyword allows reassignment?",
   {"main.go": """// 010: const values cannot be reassigned; use var (or :=)
// for things that change. TODO: fix the error; print 2.
package main

import "fmt"

func main() {
\tconst x = 1
\tx = 2
\tfmt.Println(x)
}
"""},
   {"main.go": """// 010: const values cannot be reassigned; use var (or :=)
// for things that change.
package main

import "fmt"

func main() {
\tvar x = 1
\tx = 2
\tfmt.Println(x)
}
"""},
   expected="2")

# 011 if_init
ex("011_if_init", "control-flow", "test",
   "Look at which branch runs for a failing score.",
   {"main.go": """// 011: if can run a short statement before the condition, scoped
// to the branches: if s := score; s >= 60 { ... }.
// TODO: return "fail" for scores below 60.
package main

func Grade(score int) string {
\tif s := score; s >= 60 {
\t\treturn "pass"
\t}
\treturn "pass"
}
"""},
   {"main.go": """// 011: if can run a short statement before the condition, scoped
// to the branches: if s := score; s >= 60 { ... }.
package main

func Grade(score int) string {
\tif s := score; s >= 60 {
\t\treturn "pass"
\t}
\treturn "fail"
}
"""},
   {"exercise_test.go": """package main

import "testing"

func TestGrade(t *testing.T) {
\tif Grade(90) != "pass" {
\t\tt.Fatal("90 should pass")
\t}
\tif Grade(30) != "fail" {
\t\tt.Fatal("30 should fail")
\t}
}
"""})

# 012 switch_basic
ex("012_switch_basic", "control-flow", "test",
   "Which case matches 1? What should each case return?",
   {"main.go": """// 012: switch picks the first matching case. No break needed.
// TODO: return the short day names below.
package main

func Day(n int) string {
\tswitch n {
\tcase 1:
\t\treturn "Monday"
\tcase 2:
\t\treturn "Tuesday"
\tdefault:
\t\treturn "?"
\t}
}
"""},
   {"main.go": """// 012: switch picks the first matching case. No break needed.
package main

func Day(n int) string {
\tswitch n {
\tcase 1:
\t\treturn "Mon"
\tcase 2:
\t\treturn "Tue"
\tdefault:
\t\treturn "?"
\t}
}
"""},
   {"exercise_test.go": """package main

import "testing"

func TestDay(t *testing.T) {
\tif Day(1) != "Mon" {
\t\tt.Fatalf("got %q want Mon", Day(1))
\t}
\tif Day(2) != "Tue" {
\t\tt.Fatalf("got %q want Tue", Day(2))
\t}
\tif Day(9) != "?" {
\t\tt.Fatalf("got %q want ?", Day(9))
\t}
}
"""})

# 013 switch_no_fallthrough
ex("013_switch_fallthrough", "control-flow", "test",
   "Does Go fall through by default? Is that keyword helping here?",
   {"main.go": """// 013: Go cases do NOT fall through; the keyword fallthrough is
// opt-in and usually a smell. TODO: fix the wrong grade for 85.
// Hint: trace case 85 with the fallthrough.
package main

func Letter(score int) string {
\tswitch {
\tcase score >= 90:
\t\treturn "A"
\tcase score >= 80:
\t\tfallthrough
\tcase score >= 70:
\t\treturn "C"
\tdefault:
\t\treturn "F"
\t}
}
"""},
   {"main.go": """// 013: Go cases do NOT fall through; the keyword fallthrough is
// opt-in and usually a smell.
package main

func Letter(score int) string {
\tswitch {
\tcase score >= 90:
\t\treturn "A"
\tcase score >= 80:
\t\treturn "B"
\tcase score >= 70:
\t\treturn "C"
\tdefault:
\t\treturn "F"
\t}
}
"""},
   {"exercise_test.go": """package main

import "testing"

func TestLetter(t *testing.T) {
\tcases := map[int]string{95: "A", 85: "B", 75: "C", 10: "F"}
\tfor in, want := range cases {
\t\tif got := Letter(in); got != want {
\t\t\tt.Fatalf("Letter(%d)=%q want %q", in, got, want)
\t\t}
\t}
}
"""})

# 014 type_switch
ex("014_type_switch", "control-flow", "test",
   "What happens when v holds an int and you assert v.(string)?",
   {"main.go": """// 014: A type switch branches on dynamic type safely:
// switch x := v.(type) { case string: ... case int: ... }.
// TODO: handle both string and int without panicking.
package main

import "fmt"

func Describe(v any) string {
\ts := v.(string)
\treturn "str:" + s
}
"""},
   {"main.go": """// 014: A type switch branches on dynamic type safely:
// switch x := v.(type) { case string: ... case int: ... }.
package main

import "fmt"

func Describe(v any) string {
\tswitch x := v.(type) {
\tcase string:
\t\treturn "str:" + x
\tcase int:
\t\treturn fmt.Sprintf("int:%d", x)
\tdefault:
\t\treturn "?"
\t}
}
"""},
   {"exercise_test.go": """package main

import "testing"

func TestDescribe(t *testing.T) {
\tif Describe("hi") != "str:hi" {
\t\tt.Fatalf("got %q", Describe("hi"))
\t}
\tif Describe(42) != "int:42" {
\t\tt.Fatalf("got %q", Describe(42))
\t}
}
"""})

# 015 for_only_loop
ex("015_for_loop", "control-flow", "test",
   "Should the loop include n itself? Check the condition.",
   {"main.go": """// 015: for is the only loop. `for i := 1; i <= n; i++` sums 1..n.
// TODO: include n in the sum.
package main

func SumTo(n int) int {
\tsum := 0
\tfor i := 1; i < n; i++ {
\t\tsum += i
\t}
\treturn sum
}
"""},
   {"main.go": """// 015: for is the only loop. `for i := 1; i <= n; i++` sums 1..n.
package main

func SumTo(n int) int {
\tsum := 0
\tfor i := 1; i <= n; i++ {
\t\tsum += i
\t}
\treturn sum
}
"""},
   {"exercise_test.go": """package main

import "testing"

func TestSumTo(t *testing.T) {
\tif SumTo(5) != 15 {
\t\tt.Fatalf("got %d want 15", SumTo(5))
\t}
\tif SumTo(1) != 1 {
\t\tt.Fatalf("got %d want 1", SumTo(1))
\t}
}
"""})

# 016 range_slice
ex("016_range_slice", "control-flow", "test",
   "When you range with two vars, what is each one a copy of?",
   {"main.go": """// 016: `for i, v := range s` copies each element into v.
// Assigning to v does not touch the slice; use s[i].
// TODO: double the elements in place.
package main

func Double(ns []int) []int {
\tfor _, v := range ns {
\t\tv *= 2
\t}
\treturn ns
}
"""},
   {"main.go": """// 016: `for i, v := range s` copies each element into v.
// Assigning to v does not touch the slice; use s[i].
package main

func Double(ns []int) []int {
\tfor i := range ns {
\t\tns[i] *= 2
\t}
\treturn ns
}
"""},
   {"exercise_test.go": """package main

import (
\t"reflect"
\t"testing"
)

func TestDouble(t *testing.T) {
\tif got := Double([]int{1, 2, 3}); !reflect.DeepEqual(got, []int{2, 4, 6}) {
\t\tt.Fatalf("got %v", got)
\t}
}
"""})

# 017 range_int (Go 1.22)
ex("017_range_int", "control-flow", "test",
   "How many values does `for i := range n` yield? Compare with <=.",
   {"main.go": """// 017: Since Go 1.22 you can range directly over an integer:
// `for i := range n` yields 0..n-1 (n values total).
// TODO: return exactly n values: 0..n-1.
package main

func First(n int) []int {
\tvar out []int
\tfor i := 0; i <= n; i++ {
\t\tout = append(out, i)
\t}
\treturn out
}
"""},
   {"main.go": """// 017: Since Go 1.22 you can range directly over an integer:
// `for i := range n` yields 0..n-1 (n values total).
package main

func First(n int) []int {
\tvar out []int
\tfor i := range n {
\t\tout = append(out, i)
\t}
\treturn out
}
"""},
   {"exercise_test.go": """package main

import (
\t"reflect"
\t"testing"
)

func TestFirst(t *testing.T) {
\tif got := First(4); !reflect.DeepEqual(got, []int{0, 1, 2, 3}) {
\t\tt.Fatalf("got %v", got)
\t}
}
"""})

# 018 labels
ex("018_labels", "control-flow", "test",
   "Which loop does plain break exit? How do you exit both?",
   {"main.go": """// 018: Labels let break/continue target an outer loop:
// outer: for ... { for ... { break outer } }.
// TODO: stop both loops once the target is found.
package main

func Find(target int, m [][]int) (int, int, bool) {
\tfor i := range m {
\t\tfor j := range m[i] {
\t\t\tif m[i][j] == target {
\t\t\t\tbreak
\t\t\t}
\t\t}
\t}
\treturn 0, 0, false
}
"""},
   {"main.go": """// 018: Labels let break/continue target an outer loop:
// outer: for ... { for ... { break outer } }.
package main

func Find(target int, m [][]int) (int, int, bool) {
\tfr, fc := 0, 0
\tfound := false
outer:
\tfor i := range m {
\t\tfor j := range m[i] {
\t\t\tif m[i][j] == target {
\t\t\t\tfr, fc, found = i, j, true
\t\t\t\tbreak outer
\t\t\t}
\t\t}
\t}
\treturn fr, fc, found
}
""" },
   {"exercise_test.go": """package main

import "testing"

func TestFind(t *testing.T) {
\tm := [][]int{{1, 2}, {3, 4}}
\tr, c, ok := Find(4, m)
\tif !ok || r != 1 || c != 1 {
\t\tt.Fatalf("got %d,%d,%v", r, c, ok)
\t}
\tif _, _, ok := Find(9, m); ok {
\t\tt.Fatal("should not find 9")
\t}
}
"""})

# 019 defer_lifo
ex("019_defer_lifo", "control-flow", "run",
   "When do deferred calls run, and in what order?",
   {"main.go": """// 019: defer schedules a call for when the function returns.
// Deferred calls run LIFO: last deferred, first executed.
// TODO: print 321 using three deferred Print calls.
package main

import "fmt"

func main() {
\tfmt.Print(1)
\tfmt.Print(2)
\tfmt.Print(3)
\tfmt.Println()
}
"""},
   {"main.go": """// 019: defer schedules a call for when the function returns.
// Deferred calls run LIFO: last deferred, first executed.
package main

import "fmt"

func main() {
\tdefer fmt.Print(1)
\tdefer fmt.Print(2)
\tdefer fmt.Print(3)
}
"""},
   expected="321")

# fix 019 solution: deferred Prints have no newline; go run output "321" (no newline) -> TrimSpace ok.
# But solution prints nothing else; need newline? TrimSpace handles it.

# 020 defer_loop
ex("020_defer_in_loop", "control-flow", "test",
   "When does a defer inside a loop run? What does that do to maxOpen?",
   {"main.go": """// 020: GOTCHA: defer inside a loop waits until the FUNCTION returns,
// not the iteration. For files/locks in loops, close explicitly.
// TODO: keep at most 1 slot open at a time.
package main

func MaxOpen(n int) int {
\topen, max := 0, 0
\tfor i := 0; i < n; i++ {
\t\topen++
\t\tif open > max {
\t\t\tmax = open
\t\t}
\t\tdefer func() { open-- }()
\t}
\treturn max
}
"""},
   {"main.go": """// 020: GOTCHA: defer inside a loop waits until the FUNCTION returns,
// not the iteration. For files/locks in loops, close explicitly.
package main

func MaxOpen(n int) int {
\topen, max := 0, 0
\tfor i := 0; i < n; i++ {
\t\topen++
\t\tif open > max {
\t\t\tmax = open
\t\t}
\t\topen-- // close/end of iteration: do not defer in a loop
\t}
\treturn max
}
"""},
   {"exercise_test.go": """package main

import "testing"

func TestMaxOpen(t *testing.T) {
\tif got := MaxOpen(5); got != 1 {
\t\tt.Fatalf("got maxOpen=%d want 1", got)
\t}
}
"""})

# 021 multiple_returns
ex("021_multiple_returns", "functions", "test",
   "Which part is returned first? Check the order.",
   {"main.go": """// 021: Functions can return several values: func f() (int, error).
// Comma-separated returns power the (value, error) idiom.
// TODO: return host first, then port.
package main

import "strings"

func SplitHostPort(s string) (string, string) {
\tparts := strings.SplitN(s, ":", 2)
\tif len(parts) != 2 {
\t\treturn "", ""
\t}
\treturn parts[1], parts[0]
}
"""},
   {"main.go": """// 021: Functions can return several values: func f() (int, error).
// Comma-separated returns power the (value, error) idiom.
package main

import "strings"

func SplitHostPort(s string) (string, string) {
\tparts := strings.SplitN(s, ":", 2)
\tif len(parts) != 2 {
\t\treturn "", ""
\t}
\treturn parts[0], parts[1]
}
"""},
   {"exercise_test.go": """package main

import "testing"

func TestSplit(t *testing.T) {
\th, p := SplitHostPort("localhost:8080")
\tif h != "localhost" || p != "8080" {
\t\tt.Fatalf("got %q,%q", h, p)
\t}
}
"""})

# 022 named_returns
ex("022_named_returns", "functions", "test",
   "Which named result should get which input?",
   {"main.go": """// 022: Named results are pre-declared locals; bare `return`
// returns them as-is. Use for short funcs, not as documentation.
// TODO: actually swap a and b.
package main

func Swap(a, b int) (x, y int) {
\tx = a
\ty = b
\treturn
}
"""},
   {"main.go": """// 022: Named results are pre-declared locals; bare `return`
// returns them as-is. Use for short funcs, not as documentation.
package main

func Swap(a, b int) (x, y int) {
\tx = b
\ty = a
\treturn
}
"""},
   {"exercise_test.go": """package main

import "testing"

func TestSwap(t *testing.T) {
\tx, y := Swap(1, 2)
\tif x != 2 || y != 1 {
\t\tt.Fatalf("got %d,%d", x, y)
\t}
}
"""})

# 023 variadics
ex("023_variadics", "functions", "test",
   "What does nums hold inside the function? What should you total?",
   {"main.go": """// 023: Variadics take any number of args as a slice: f(nums ...int).
// Call with f(1,2) or f(slice...).
// TODO: return the sum, not the count.
package main

func Sum(nums ...int) int {
\treturn len(nums)
}
"""},
   {"main.go": """// 023: Variadics take any number of args as a slice: f(nums ...int).
// Call with f(1,2) or f(slice...).
package main

func Sum(nums ...int) int {
\ttotal := 0
\tfor _, n := range nums {
\t\ttotal += n
\t}
\treturn total
}
"""},
   {"exercise_test.go": """package main

import "testing"

func TestSum(t *testing.T) {
\tif Sum(1, 2, 3) != 6 {
\t\tt.Fatalf("got %d", Sum(1, 2, 3))
\t}
\tif Sum() != 0 {
\t\tt.Fatal("empty sum should be 0")
\t}
\ts := []int{4, 5}
\tif Sum(s...) != 9 {
\t\tt.Fatal("spread call failed")
\t}
}
"""})

# 024 closures
ex("024_closures", "functions", "test",
   "What state does the returned func close over?",
   {"main.go": """// 024: Closures capture surrounding variables by reference.
// Each call to Counter must keep its own state.
// TODO: return a func counting 1,2,3... per call.
package main

func Counter() func() int {
\treturn func() int {
\t\treturn 0
\t}
}
"""},
   {"main.go": """// 024: Closures capture surrounding variables by reference.
// Each call to Counter must keep its own state.
package main

func Counter() func() int {
\tn := 0
\treturn func() int {
\t\tn++
\t\treturn n
\t}
}
"""},
   {"exercise_test.go": """package main

import "testing"

func TestCounter(t *testing.T) {
\tc := Counter()
\tfor want := 1; want <= 3; want++ {
\t\tif got := c(); got != want {
\t\t\tt.Fatalf("got %d want %d", got, want)
\t\t}
\t}
}
"""})

# 025 func_values
ex("025_func_values", "functions", "test",
   "What is f for? When should it be called?",
   {"main.go": """// 025: Functions are values: pass them, store them, call them.
// TODO: apply f to v.
package main

func Apply(f func(int) int, v int) int {
\treturn v
}
"""},
   {"main.go": """// 025: Functions are values: pass them, store them, call them.
package main

func Apply(f func(int) int, v int) int {
\treturn f(v)
}
"""},
   {"exercise_test.go": """package main

import "testing"

func TestApply(t *testing.T) {
\tdouble := func(n int) int { return 2 * n }
\tif Apply(double, 3) != 6 {
\t\tt.Fatal("Apply should call f")
\t}
}
"""})

# 026 methods_as_values (value vs pointer preview)
ex("026_method_values", "functions", "test",
   "Does Inc actually mutate the counter? Check the receiver.",
   {"main.go": """// 026: Methods are functions with a receiver. A method value like
// f := c.Inc keeps the receiver bound; pointer receivers mutate.
// TODO: make Inc increment the counter.
package main

type Counter2 struct{ N int }

func (c Counter2) Inc() { c.N++ }

func TwoIncs() int {
\tc := &Counter2{}
\tf := c.Inc
\tf()
\tf()
\treturn c.N
}
"""},
   {"main.go": """// 026: Methods are functions with a receiver. A method value like
// f := c.Inc keeps the receiver bound; pointer receivers mutate.
package main

type Counter2 struct{ N int }

func (c *Counter2) Inc() { c.N++ }

func TwoIncs() int {
\tc := &Counter2{}
\tf := c.Inc
\tf()
\tf()
\treturn c.N
}
"""},
   {"exercise_test.go": """package main

import "testing"

func TestTwoIncs(t *testing.T) {
\tif TwoIncs() != 2 {
\t\tt.Fatalf("got %d want 2", TwoIncs())
\t}
}
"""})

print(f"batch1: {len([1])} marker")
