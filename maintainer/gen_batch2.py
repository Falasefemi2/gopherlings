"""Batch 2: collections, strings, structs, pointers, interfaces (027-055)."""
import sys
sys.path.insert(0, ".")
from genlib import add_manifest, write_files

def ex(edir, topic, mode, hint, ex_files, sol_files, test_files=None, expected=None):
    num = edir.split("_")[0]
    add_manifest(num, edir, mode, hint, topic, expected)
    write_files(edir, {"ex": ex_files, "sol": sol_files, "test": test_files})

# ---- collections ----
ex("027_arrays_slices", "collections", "test",
   "Is [3]int the same type as []int? Which one can grow?",
   {"main.go": """// 027: Arrays have fixed length ([3]int); slices are views over
// arrays and can grow. Most Go code uses slices ([]int).
// TODO: return the slice 1..3 with length 3.
package main

func Nums() [3]int {
\treturn [3]int{1, 2, 3}
}
"""},
   {"main.go": """// 027: Arrays have fixed length ([3]int); slices are views over
// arrays and can grow. Most Go code uses slices ([]int).
package main

func Nums() []int {
\treturn []int{1, 2, 3}
}
"""},
   {"exercise_test.go": """package main

import (
\t"reflect"
\t"testing"
)

func TestNums(t *testing.T) {
\tif got := Nums(); !reflect.DeepEqual(got, []int{1, 2, 3}) {
\t\tt.Fatalf("got %#v", got)
\t}
}
"""})
# NOTE: broken returns [3]int but test compares to []int via DeepEqual -> fails
# (DeepEqual([3]int, []int) is false). Solution returns []int. Good.

ex("028_len_cap", "collections", "test",
   "What do len and cap report for make([]int, 2, 5)?",
   {"main.go": """// 028: len is usable elements; cap is backing-array size.
// make([]int, 2, 5) has len 2, cap 5. append grows up to cap.
// TODO: report the real len and cap.
package main

func LenCap() (int, int) {
\ts := make([]int, 2, 5)
\t_ = s
\treturn 5, 2
}
"""},
   {"main.go": """// 028: len is usable elements; cap is backing-array size.
// make([]int, 2, 5) has len 2, cap 5. append grows up to cap.
package main

func LenCap() (int, int) {
\ts := make([]int, 2, 5)
\treturn len(s), cap(s)
}
"""},
   {"exercise_test.go": """package main

import "testing"

func TestLenCap(t *testing.T) {
\tl, c := LenCap()
\tif l != 2 || c != 5 {
\t\tt.Fatalf("got len=%d cap=%d", l, c)
\t}
}
"""})

ex("029_append_alias", "collections", "test",
   "Do a and b share a backing array? What does append reuse?",
   {"main.go": """// 029: GOTCHA: slices share backing arrays. append may reuse it,
// so one slice's update can clobber another's. Copy to isolate.
// TODO: make Double return a new slice, leaving the input intact.
package main

func DoubleAll(ns []int) []int {
\tout := ns[:0]
\tfor _, v := range ns {
\t\tout = append(out, v*2)
\t}
\treturn out
}
"""},
   {"main.go": """// 029: GOTCHA: slices share backing arrays. append may reuse it,
// so one slice's update can clobber another's. Copy to isolate.
package main

func DoubleAll(ns []int) []int {
\tout := make([]int, len(ns))
\tfor i, v := range ns {
\t\tout[i] = v * 2
\t}
\treturn out
}
"""},
   {"exercise_test.go": """package main

import (
\t"reflect"
\t"testing"
)

func TestDoubleAll(t *testing.T) {
\tin := []int{1, 2, 3}
\tgot := DoubleAll(in)
\tif !reflect.DeepEqual(got, []int{2, 4, 6}) {
\t\tt.Fatalf("got %v", got)
\t}
\tif !reflect.DeepEqual(in, []int{1, 2, 3}) {
\t\tt.Fatalf("input was clobbered: %v", in)
\t}
}
"""})
# broken: ns[:0] reuses array, writes doubled values into in -> in becomes [2,4,6], second check fails. Good.

ex("030_nil_map_write", "collections", "test",
   "What is the zero value of a map? Can you write to it?",
   {"main.go": """// 030: GOTCHA: a nil map reads fine but writing panics.
// Declare with make or a literal before inserting.
// TODO: stop the panic when inserting.
package main

func Put(m map[string]int, k string, v int) map[string]int {
\tm[k] = v
\treturn m
}
"""},
   {"main.go": """// 030: GOTCHA: a nil map reads fine but writing panics.
// Declare with make or a literal before inserting.
package main

func Put(m map[string]int, k string, v int) map[string]int {
\tif m == nil {
\t\tm = make(map[string]int)
\t}
\tm[k] = v
\treturn m
}
"""},
   {"exercise_test.go": """package main

import "testing"

func TestPutNil(t *testing.T) {
\tdefer func() {
\t\tif r := recover(); r != nil {
\t\t\tt.Fatalf("panicked on nil map write: %v", r)
\t\t}
\t}()
\tm := Put(nil, "a", 1)
\tif m["a"] != 1 {
\t\tt.Fatalf("got %v", m)
\t}
}
"""})

ex("031_comma_ok", "collections", "test",
   "How do you tell a stored zero from a missing key?",
   {"main.go": """// 031: Map lookup returns (value, ok). ok reports presence;
// without it a missing key looks like a stored zero value.
// TODO: report whether the key exists.
package main

func Lookup(m map[string]int, k string) (int, bool) {
\treturn m[k], true
}
"""},
   {"main.go": """// 031: Map lookup returns (value, ok). ok reports presence;
// without it a missing key looks like a stored zero value.
package main

func Lookup(m map[string]int, k string) (int, bool) {
\tv, ok := m[k]
\treturn v, ok
}
"""},
   {"exercise_test.go": """package main

import "testing"

func TestLookup(t *testing.T) {
\tm := map[string]int{"a": 0}
\tif _, ok := Lookup(m, "missing"); ok {
\t\tt.Fatal("missing key should report ok=false")
\t}
\tif v, ok := Lookup(m, "a"); !ok || v != 0 {
\t\tt.Fatalf("got %d,%v", v, ok)
\t}
}
"""})

ex("032_map_order", "collections", "test",
   "Is map iteration order deterministic? How do you get sorted keys?",
   {"main.go": """// 032: Map iteration order is randomized on purpose. For stable
// output, collect keys and sort them (slices.SortedKeys / Sort).
// TODO: return keys in sorted order.
package main

import "sort"

func Keys(m map[string]int) []string {
\tout := make([]string, 0, len(m))
\tfor k := range m {
\t\tout = append(out, k)
\t}
\t_ = sort.Strings
\treturn out
}
"""},
   {"main.go": """// 032: Map iteration order is randomized on purpose. For stable
// output, collect keys and sort them (slices.SortedKeys / Sort).
package main

import "sort"

func Keys(m map[string]int) []string {
\tout := make([]string, 0, len(m))
\tfor k := range m {
\t\tout = append(out, k)
\t}
\tsort.Strings(out)
\treturn out
}
"""},
   {"exercise_test.go": """package main

import (
\t"reflect"
\t"testing"
)

func TestKeys(t *testing.T) {
\tm := map[string]int{"h": 8, "e": 5, "c": 3, "a": 1, "d": 4, "b": 2, "g": 7, "f": 6}
\tif got := Keys(m); !reflect.DeepEqual(got, []string{"a", "b", "c", "d", "e", "f", "g", "h"}) {
\t\tt.Fatalf("got %v", got)
\t}
}
"""})
# broken imports sort but only references sort.Strings without calling -> compiles (assigned to _), returns unsorted (usually). Test may flake if random order happens to be sorted. With 3 keys, 1/6 chance of accidental pass! Fix: use more keys to reduce flake: 5 keys -> 1/120 chance. Let's use 5 keys. Edit test to 5 keys.

ex("033_slices_pkg", "collections", "test",
   "Which stdlib package sorts a slice without writing the loop?",
   {"main.go": """// 033: The slices package (Go 1.21+) has Sort, Compact, Clone,
// SortedKeys and friends. Prefer it over hand-rolled loops.
// TODO: return the sorted copy.
package main

func Sorted(ns []int) []int {
\treturn ns
}
"""},
   {"main.go": """// 033: The slices package (Go 1.21+) has Sort, Compact, Clone,
// SortedKeys and friends. Prefer it over hand-rolled loops.
package main

import "slices"

func Sorted(ns []int) []int {
\tout := slices.Clone(ns)
\tslices.Sort(out)
\treturn out
}
"""},
   {"exercise_test.go": """package main

import (
\t"reflect"
\t"testing"
)

func TestSorted(t *testing.T) {
\tif got := Sorted([]int{3, 1, 2}); !reflect.DeepEqual(got, []int{1, 2, 3}) {
\t\tt.Fatalf("got %v", got)
\t}
}
"""})

ex("034_maps_pkg", "collections", "test",
   "Which stdlib package clones a map in one call?",
   {"main.go": """// 034: The maps package (Go 1.21+) has Clone, Equal, Keys, Merge
// style helpers. TODO: return an equal but independent copy.
package main

func Clone(m map[string]int) map[string]int {
\treturn m
}
"""},
   {"main.go": """// 034: The maps package (Go 1.21+) has Clone, Equal, Keys, Merge
// style helpers.
package main

import "maps"

func Clone(m map[string]int) map[string]int {
\treturn maps.Clone(m)
}
"""},
   {"exercise_test.go": """package main

import (
\t"maps"
\t"testing"
)

func TestClone(t *testing.T) {
\tsrc := map[string]int{"a": 1}
\tgot := Clone(src)
\tif !maps.Equal(got, src) {
\t\tt.Fatalf("got %v", got)
\t}
\tgot["a"] = 99
\tif src["a"] != 1 {
\t\tt.Fatal("clone shares storage with source")
\t}
}
"""})
# broken returns same map -> mutation leaks -> second check fails. Good.

ex("035_slice_expr", "collections", "test",
   "What does s[1:3] share with s? Where does append write?",
   {"main.go": """// 035: Slice expressions share storage: s[1:3] aliases s.
// Full slice expr s[1:3:3] caps capacity to prevent append clobber.
// TODO: append without clobbering the original's tail.
package main

func AppendFirstTwo(s []int, extra int) []int {
\tsub := s[:2]
\tsub = append(sub, extra)
\treturn sub
}
"""},
   {"main.go": """// 035: Slice expressions share storage: s[1:3] aliases s.
// Full slice expr s[1:3:3] caps capacity to prevent append clobber.
package main

func AppendFirstTwo(s []int, extra int) []int {
\tsub := s[:2:2]
\tsub = append(sub, extra)
\treturn sub
}
"""},
   {"exercise_test.go": """package main

import (
\t"reflect"
\t"testing"
)

func TestAppendFirstTwo(t *testing.T) {
\ts := []int{1, 2, 3}
\tgot := AppendFirstTwo(s, 9)
\tif !reflect.DeepEqual(got, []int{1, 2, 9}) {
\t\tt.Fatalf("got %v", got)
\t}
\tif !reflect.DeepEqual(s, []int{1, 2, 3}) {
\t\tt.Fatalf("source clobbered: %v", s)
\t}
}
"""})
# broken: s has len3 cap3? literal []int{1,2,3} cap==3, s[:2] cap==3, append writes index2 -> clobbers s[2] to 9 -> source becomes [1,2,9]. Fails second check. Fixed with full expr cap2 forces realloc. Good deterministic.

# ---- strings ----
ex("036_bytes_runes", "strings", "test",
   "Is len(s) bytes or characters? What does ranging yield?",
   {"main.go": """// 036: string is bytes; len counts bytes, not characters (runes).
// range decodes UTF-8 runes; indexing gives single bytes.
// TODO: count characters (runes), not bytes.
package main

func RuneLen(s string) int {
\treturn len(s)
}
"""},
   {"main.go": """// 036: string is bytes; len counts bytes, not characters (runes).
// range decodes UTF-8 runes; indexing gives single bytes.
package main

func RuneLen(s string) int {
\tn := 0
\tfor range s {
\t\tn++
\t}
\treturn n
}
"""},
   {"exercise_test.go": """package main

import "testing"

func TestRuneLen(t *testing.T) {
\tif RuneLen("héllo") != 5 {
\t\tt.Fatalf("got %d want 5", RuneLen("héllo"))
\t}
\tif RuneLen("go") != 2 {
\t\tt.Fatal("ascii failed")
\t}
}
"""})
# "héllo": é is 2 bytes, len=6, runes=5. Good.

ex("037_builder", "strings", "test",
   "What is the efficient way to concatenate in a loop?",
   {"main.go": """// 037: strings.Builder concatenates without O(n^2) copies.
// WriteString in a loop, then String() once.
// TODO: join the parts efficiently.
package main

func Join(parts []string) string {
\ts := ""
\tfor _, p := range parts {
\t\ts += p
\t}
\t_ = s
\treturn "TODO"
}
"""},
   {"main.go": """// 037: strings.Builder concatenates without O(n^2) copies.
// WriteString in a loop, then String() once.
package main

import "strings"

func Join(parts []string) string {
\tvar b strings.Builder
\tfor _, p := range parts {
\t\tb.WriteString(p)
\t}
\treturn b.String()
}
"""},
   {"exercise_test.go": """package main

import "testing"

func TestJoin(t *testing.T) {
\tif Join([]string{"a", "b", "c"}) != "abc" {
\t\tt.Fatalf("got %q", Join([]string{"a", "b", "c"}))
\t}
\tif Join(nil) != "" {
\t\tt.Fatal("nil should join to empty")
\t}
}
"""})

ex("038_strconv", "strings", "test",
   "Which strconv func parses, and what else does it return?",
   {"main.go": """// 038: strconv converts text<->numbers: Atoi, Itoa, ParseInt,
// ParseFloat, Quote. Most return (value, error); check it.
// TODO: parse the decimal string, returning errors properly.
package main

import "strconv"

func ParseAge(s string) (int, error) {
\tn, _ := strconv.Atoi(s)
\treturn n, nil
}
"""},
   {"main.go": """// 038: strconv converts text<->numbers: Atoi, Itoa, ParseInt,
// ParseFloat, Quote. Most return (value, error); check it.
package main

import "strconv"

func ParseAge(s string) (int, error) {
\treturn strconv.Atoi(s)
}
"""},
   {"exercise_test.go": """package main

import "testing"

func TestParseAge(t *testing.T) {
\tif n, err := ParseAge("42"); err != nil || n != 42 {
\t\tt.Fatalf("got %d,%v", n, err)
\t}
\tif _, err := ParseAge("abc"); err == nil {
\t\tt.Fatal("expected error for abc")
\t}
}
"""})
# broken swallows error -> second check fails. Good (shadowed/ignored err preview).

ex("039_utf8", "strings", "test",
   "How do you decode the first rune and its width?",
   {"main.go": """// 039: utf8.DecodeRuneInString returns (rune, width). Indexing
// s[0] is just the first byte, wrong for multibyte runes.
// TODO: return the first rune of s.
package main

import "unicode/utf8"

func FirstRune(s string) rune {
\tr, _ := utf8.DecodeRuneInString(s)
\t_ = r
\treturn rune(s[0])
}
"""},
   {"main.go": """// 039: utf8.DecodeRuneInString returns (rune, width). Indexing
// s[0] is just the first byte, wrong for multibyte runes.
package main

import "unicode/utf8"

func FirstRune(s string) rune {
\tr, _ := utf8.DecodeRuneInString(s)
\treturn r
}
"""},
   {"exercise_test.go": """package main

import "testing"

func TestFirstRune(t *testing.T) {
\tif FirstRune("éclair") != 'é' {
\t\tt.Fatalf("got %q", FirstRune("éclair"))
\t}
}
"""})
# broken returns rune(byte) -> 0xC3 (195) vs 'é' (233). Fails. But `return byte(s[0])` with return type rune: byte converts to rune implicitly? byte is uint8, func returns rune: `return byte(s[0])` - Go auto converts? No, need explicit? Actually return type rune, returning byte value: assignable? byte->rune requires conversion? Go assignability: x of type V assignable to T if V and T have identical underlying and one is not named? byte underlying uint8, rune underlying int32 - different, so NOT assignable. Compile error! Fix to `return rune(s[0])`? That compiles but wrong value. Let's make broken `return rune(s[0])` so it compiles but fails test.

# ---- structs ----
ex("040_struct_literal", "structs", "test",
   "Which literal form breaks when a field is added?",
   {"main.go": """// 040: Prefer keyed literals (Point{X:1}) over positional ones.
// Keyed literals survive new fields; positional ones do not.
// TODO: build Point{X:1, Y:2} with field names.
package main

type Point struct{ X, Y int }

func Origin() Point {
\treturn Point{0, 0}
}

func P() Point {
\treturn Point{2, 1}
}
"""},
   {"main.go": """// 040: Prefer keyed literals (Point{X:1}) over positional ones.
// Keyed literals survive new fields; positional ones do not.
package main

type Point struct{ X, Y int }

func Origin() Point {
\treturn Point{X: 0, Y: 0}
}

func P() Point {
\treturn Point{X: 1, Y: 2}
}
"""},
   {"exercise_test.go": """package main

import "testing"

func TestP(t *testing.T) {
\tp := P()
\tif p.X != 1 || p.Y != 2 {
\t\tt.Fatalf("got %+v", p)
\t}
}
"""})
# broken P returns {2,1} swapped -> fails. Good. Origin unused ok.

ex("041_receivers", "structs", "test",
   "Should Scale mutate the struct? Which receiver allows that?",
   {"main.go": """// 041: Value receivers copy; pointer receivers mutate. Use pointer
// for mutation or large structs, value for small immutable ones.
// TODO: make Scale actually scale the rectangle.
package main

type Rect struct{ W, H int }

func (r Rect) Scale(k int) { r.W *= k; r.H *= k }

func Scaled() Rect {
\tr := Rect{W: 2, H: 3}
\tr.Scale(10)
\treturn r
}
"""},
   {"main.go": """// 041: Value receivers copy; pointer receivers mutate. Use pointer
// for mutation or large structs, value for small immutable ones.
package main

type Rect struct{ W, H int }

func (r *Rect) Scale(k int) { r.W *= k; r.H *= k }

func Scaled() Rect {
\tr := Rect{W: 2, H: 3}
\tr.Scale(10)
\treturn r
}
"""},
   {"exercise_test.go": """package main

import "testing"

func TestScaled(t *testing.T) {
\tif got := Scaled(); got.W != 20 || got.H != 30 {
\t\tt.Fatalf("got %+v", got)
\t}
}
"""})
# fix comment typo: "value for value for" -> fix.

ex("042_embedding", "structs", "test",
   "How do promoted methods reach the outer struct?",
   {"main.go": """// 042: Embedding composes behavior: outer structs promote the
// embedded type's methods. No inheritance, just composition.
// TODO: make Logger available on Server via embedding.
package main

type Logger struct{}

func (Logger) Log(s string) string { return "log:" + s }

type Server struct {
\t*Logger
\tName string
}

func NewServer() *Server {
\treturn &Server{Name: "web"}
}
"""},
   {"main.go": """// 042: Embedding composes behavior: outer structs promote the
// embedded type's methods. No inheritance, just composition.
package main

type Logger struct{}

func (Logger) Log(s string) string { return "log:" + s }

type Server struct {
\t*Logger
\tName string
}

func NewServer() *Server {
\treturn &Server{Logger: &Logger{}, Name: "web"}
}
"""},
   {"exercise_test.go": """package main

import "testing"

func TestEmbed(t *testing.T) {
\ts := NewServer()
\tif s.Log("hi") != "log:hi" {
\t\tt.Fatal("promoted Log failed (nil embedded Logger?)")
\t}
}
"""})
# broken NewServer leaves Logger nil -> s.Log panics (nil deref)? Calling pointer method on nil *Logger? Method has value receiver (Logger), calling via nil *Logger pointer -> panic dereference. Test fails (panic). Good gotcha. Fixed initializes.

ex("043_struct_tags", "structs", "test",
   "How does encoding/json know to use lowercase keys?",
   {"main.go": """// 043: Struct tags are metadata strings; encoding/json reads
// `json:"name"` to map fields. Unexported fields are ignored.
// TODO: make JSON use lowercase keys.
package main

import "encoding/json"

type User struct {
\tName string
\tAge  int
}

func ToJSON() string {
\tb, _ := json.Marshal(User{Name: "ann", Age: 3})
\treturn string(b)
}
"""},
   {"main.go": """// 043: Struct tags are metadata strings; encoding/json reads
// `json:"name"` to map fields. Unexported fields are ignored.
package main

import "encoding/json"

type User struct {
\tName string `json:"name"`
\tAge  int    `json:"age"`
}

func ToJSON() string {
\tb, _ := json.Marshal(User{Name: "ann", Age: 3})
\treturn string(b)
}
"""},
   {"exercise_test.go": """package main

import "testing"

func TestTags(t *testing.T) {
\tif got := ToJSON(); got != `{"name":"ann","age":3}` {
\t\tt.Fatalf("got %s", got)
\t}
}
"""})
# broken produces {"Name":"ann","Age":3} -> fails. Good.

ex("044_comparable_struct", "structs", "test",
   "Which field types keep a struct comparable with ==?",
   {"main.go": """// 044: Structs with only comparable fields support == and can be
// map keys. A slice/map field makes == a compile error.
// TODO: keep the struct comparable and the equality true.
package main

type Key struct {
\tA string
\tB []int
}

func Same() bool {
\treturn Key{A: "x", B: []int{1}} == Key{A: "x", B: []int{1}}
}
"""},
   {"main.go": """// 044: Structs with only comparable fields support == and can be
// map keys. A slice/map field makes == a compile error.
package main

type Key struct {
\tA string
\tB int
}

func Same() bool {
\treturn Key{A: "x", B: 1} == Key{A: "x", B: 1}
}
"""},
   {"exercise_test.go": """package main

import "testing"

func TestSame(t *testing.T) {
\tif !Same() {
\t\tt.Fatal("expected structs to be equal")
\t}
}
"""})
# broken does not compile (invalid operation == with slice field) -> exercise fails compile. Fixed compiles+passes. Good.

ex("045_constructors", "structs", "test",
   "Why return a pointer and validate in NewUser?",
   {"main.go": """// 045: Idiom: NewT validates and returns (*T, error). Zero value
// should be useful; constructors enforce invariants.
// TODO: reject empty names with an error.
package main

import "errors"

type Account struct{ Name string }

func NewAccount(name string) (*Account, error) {
\treturn &Account{Name: name}, nil
}

var ErrName = errors.New("bad name")
"""},
   {"main.go": """// 045: Idiom: NewT validates and returns (*T, error). Zero value
// should be useful; constructors enforce invariants.
package main

import "errors"

type Account struct{ Name string }

var ErrName = errors.New("bad name")

func NewAccount(name string) (*Account, error) {
\tif name == "" {
\t\treturn nil, ErrName
\t}
\treturn &Account{Name: name}, nil
}
"""},
   {"exercise_test.go": """package main

import "testing"

func TestAccount(t *testing.T) {
\tif _, err := NewAccount(""); err == nil {
\t\tt.Fatal("expected error for empty name")
\t}
\ta, err := NewAccount("ann")
\tif err != nil || a.Name != "ann" {
\t\tt.Fatalf("got %+v,%v", a, err)
\t}
}
"""})
# broken declares ErrName but unused? It IS declared and unused package-level vars are allowed (only locals error). But `ErrName` unused at package level is fine. Good.

# ---- pointers ----
ex("046_pointers_basic", "pointers", "test",
   "What do & and * do? Which one follows the pointer?",
   {"main.go": """// 046: & takes an address, * follows it. Pointers let functions
// mutate callers and avoid copying large values.
// TODO: increment the caller's variable through the pointer.
package main

func Inc(p *int) {
\tp++
}
"""},
   {"main.go": """// 046: & takes an address, * follows it. Pointers let functions
// mutate callers and avoid copying large values.
package main

func Inc(p *int) {
\t*p++
}
"""},
   {"exercise_test.go": """package main

import "testing"

func TestInc(t *testing.T) {
\tn := 1
\tInc(&n)
\tif n != 2 {
\t\tt.Fatalf("got %d", n)
\t}
}
"""})
# broken `p++` on *int: invalid operation? p is *int, p++ is invalid (cannot increment pointer). Compile error -> exercise fails. Fixed *p++. Good.

ex("047_nil_ptr", "pointers", "test",
   "What is the zero value of a pointer? When is dereference safe?",
   {"main.go": """// 047: The zero value of any pointer is nil. Dereferencing nil
// panics; always check before following.
// TODO: return 0 for nil instead of panicking.
package main

func Deref(p *int) int {
\treturn *p
}
"""},
   {"main.go": """// 047: The zero value of any pointer is nil. Dereferencing nil
// panics; always check before following.
package main

func Deref(p *int) int {
\tif p == nil {
\t\treturn 0
\t}
\treturn *p
}
"""},
   {"exercise_test.go": """package main

import "testing"

func TestDeref(t *testing.T) {
\tif Deref(nil) != 0 {
\t\tt.Fatal("nil should give 0")
\t}
\tn := 7
\tif Deref(&n) != 7 {
\t\tt.Fatal("non-nil failed")
\t}
}
"""})
# broken panics on nil -> test fails (panic). But test calls Deref(nil) first -> panic aborts test -> fail. Good.

ex("048_mutate_via_ptr", "pointers", "test",
   "Who sees the change when you reassign the pointer vs the pointee?",
   {"main.go": """// 048: Reassigning the pointer (p = &x) only changes the local
// copy. To affect the caller, assign through it: *p = ....
// TODO: set the caller's value to 99.
package main

func Set(p *int) {
\tx := 99
\tp = &x
}
"""},
   {"main.go": """// 048: Reassigning the pointer (p = &x) only changes the local
// copy. To affect the caller, assign through it: *p = ....
package main

func Set(p *int) {
\t*p = 99
}
"""},
   {"exercise_test.go": """package main

import "testing"

func TestSet(t *testing.T) {
\tn := 0
\tSet(&n)
\tif n != 99 {
\t\tt.Fatalf("got %d", n)
\t}
}
"""})

# ---- interfaces ----
ex("049_iface_implicit", "interfaces", "test",
   "Where is the `implements` keyword? How does the compiler check it?",
   {"main.go": """// 049: Interfaces are satisfied implicitly: no `implements` keyword.
// A type satisfies Greeter by having Greet() string with that signature.
// TODO: give Loud a Greet method so it satisfies Greeter.
package main

type Greeter interface{ Greet() string }

type Loud struct{ Who string }

func Shout(g Greeter) string { return g.Greet() + "!" }

func Call() string { return Shout(Loud{Who: "bob"}) }
"""},
   {"main.go": """// 049: Interfaces are satisfied implicitly: no `implements` keyword.
// A type satisfies Greeter by having Greet() string with that signature.
package main

type Greeter interface{ Greet() string }

type Loud struct{ Who string }

func (l Loud) Greet() string { return "hi " + l.Who }

func Shout(g Greeter) string { return g.Greet() + "!" }

func Call() string { return Shout(Loud{Who: "bob"}) }
"""},
   {"exercise_test.go": """package main

import "testing"

func TestCall(t *testing.T) {
\tif Call() != "hi bob!" {
\t\tt.Fatalf("got %q", Call())
\t}
}
"""})
# broken: Loud has no Greet -> Call passes Loud as Greeter -> compile error. Good.

ex("050_any_assert", "interfaces", "test",
   "What is any an alias for? How do you get the concrete value back?",
   {"main.go": """// 050: any is an alias for interface{}. It holds anything; use a
// type assertion (v.(T)) or type switch to get values back.
// TODO: return the underlying int doubled.
package main

func DoubleAny(v any) int {
\treturn 0
}
"""},
   {"main.go": """// 050: any is an alias for interface{}. It holds anything; use a
// type assertion (v.(T)) or type switch to get values back.
package main

func DoubleAny(v any) int {
\treturn v.(int) * 2
}
"""},
   {"exercise_test.go": """package main

import "testing"

func TestDoubleAny(t *testing.T) {
\tif DoubleAny(21) != 42 {
\t\tt.Fatal("failed")
\t}
}
"""})

ex("051_type_assert_ok", "interfaces", "test",
   "What happens on a failed assertion without the ok form?",
   {"main.go": """// 051: The comma-ok assertion (x, ok := v.(T)) reports success
// instead of panicking on mismatch. Prefer it at boundaries.
// TODO: return (value, true) for ints, (0, false) otherwise.
package main

func AsInt(v any) (int, bool) {
\treturn v.(int), true
}
"""},
   {"main.go": """// 051: The comma-ok assertion (x, ok := v.(T)) reports success
// instead of panicking on mismatch. Prefer it at boundaries.
package main

func AsInt(v any) (int, bool) {
\tn, ok := v.(int)
\treturn n, ok
}
"""},
   {"exercise_test.go": """package main

import "testing"

func TestAsInt(t *testing.T) {
\tif n, ok := AsInt(5); !ok || n != 5 {
\t\tt.Fatal("int failed")
\t}
\tif _, ok := AsInt("x"); ok {
\t\tt.Fatal("string should not assert")
\t}
}
"""})
# broken panics on string -> second check panics -> fail. Good.

ex("052_nil_iface_trap", "interfaces", "test",
   "Can an interface holding a nil pointer be == nil?",
   {"main.go": """// 052: GOTCHA: an interface holding a typed nil pointer is NOT
// nil itself. Return explicit nil instead of a nil pointer.
// TODO: return nil error on success.
package main

type Boom struct{}

func (b *Boom) Error() string { return "boom" }

func Check(ok bool) error {
\tvar b *Boom
\tif ok {
\t\treturn b
\t}
\t_ = b
\treturn b
}
"""},
   {"main.go": """// 052: GOTCHA: an interface holding a typed nil pointer is NOT
// nil itself. Return explicit nil instead of a nil pointer.
package main

type Boom struct{}

func (b *Boom) Error() string { return "boom" }

func Check(ok bool) error {
\tif ok {
\t\treturn nil
\t}
\treturn &Boom{}
}
"""},
   {"exercise_test.go": """package main

import "testing"

func TestCheck(t *testing.T) {
\tif err := Check(true); err != nil {
\t\tt.Fatalf("success should be nil error, got %#v", err)
\t}
\tif err := Check(false); err == nil {
\t\tt.Fatal("failure should be non-nil")
\t}
}
"""})
# broken: Check(true) returns nil (untyped nil -> interface nil) ok; Check(false) returns b (typed nil *Boom as error, non-nil interface). Test: Check(true)==nil passes; Check(false)==nil? typed-nil interface != nil so err==nil false -> passes?? Wait test expects Check(false) non-nil: `if err := Check(false); err == nil { fail }`. Broken returns typed nil -> err != nil -> passes. So broken PASSES both! Bad. Need broken to fail: make broken return b in both branches? Actually classic trap: broken returns typed nil on SUCCESS, so Check(true) returns non-nil interface holding nil pointer -> test `err != nil` fails. Let's flip: broken code `if ok { return b }`? Currently broken: ok->return nil (correct), !ok->return b (typed nil, but test expects non-nil, and typed-nil IS non-nil so passes). So broken passes. Need to invert: success should return typed nil in broken. Change broken: `if ok { return b }`? b is nil *Boom -> non-nil error -> Check(true) != nil -> test fails. And failure branch should return... Let's redesign: broken always returns b? Simpler: broken:
#   var b *Boom  (nil)
#   if ok { return b }  // BUG: typed nil, non-nil interface
#   return b
# Then Check(true) fails. Fixed: ok->return nil, !ok->return &Boom{}. The provided fixed is that. Fix broken's ok branch to `return b`.
# Currently broken ok branch returns nil. Must edit: change to return b.

ex("053_stringer", "interfaces", "test",
   "Which method makes a type print itself with fmt?",
   {"main.go": """// 053: Implement fmt.Stringer (String() string) to control how
// fmt prints your type. It is used by Println, %v and %s.
// TODO: format as "user:<name>".
package main

import "fmt"

type Person struct{ Name string }

func Greet2(p Person) string { return fmt.Sprint(p) }
"""},
   {"main.go": """// 053: Implement fmt.Stringer (String() string) to control how
// fmt prints your type. It is used by Println, %v and %s.
package main

import "fmt"

type Person struct{ Name string }

func (p Person) String() string { return "user:" + p.Name }

func Greet2(p Person) string { return fmt.Sprint(p) }
"""},
   {"exercise_test.go": """package main

import "testing"

func TestStringer(t *testing.T) {
\tif Greet2(Person{Name: "ann"}) != "user:ann" {
\t\tt.Fatalf("got %q", Greet2(Person{Name: "ann"}))
\t}
}
"""})
# broken prints {ann} -> fails. Good.

ex("054_reader", "interfaces", "test",
   "What does Read return at end of input? How many bytes were read?",
   {"main.go": """// 054: io.Reader is Read(p []byte) (n int, err error). It returns
// io.EOF at the end; n tells how many bytes were filled.
// TODO: read at most 3 bytes and report n.
package main

import "io"

type Three struct{}

func (Three) Read(p []byte) (int, error) {
\tcopy(p, "abcdef")
\treturn 6, nil
}

func Read3(r io.Reader) (string, error) {
\tbuf := make([]byte, 3)
\tn, err := r.Read(buf)
\treturn string(buf[:n]), err
}
"""},
   {"main.go": """// 054: io.Reader is Read(p []byte) (n int, err error). It returns
// io.EOF at the end; n tells how many bytes were filled.
package main

import "io"

type Three struct{}

func (Three) Read(p []byte) (int, error) {
\tn := copy(p, "abcdef")
\tif n == 0 {
\t\treturn 0, io.EOF
\t}
\treturn n, nil
}

func Read3(r io.Reader) (string, error) {
\tbuf := make([]byte, 3)
\tn, err := r.Read(buf)
\treturn string(buf[:n]), err
}
"""},
   {"exercise_test.go": """package main

import "testing"

func TestRead3(t *testing.T) {
\ts, err := Read3(Three{})
\tif err != nil || s != "abc" {
\t\tt.Fatalf("got %q,%v", s, err)
\t}
}
"""})
# broken Read returns 6 with 3-byte buf: copy(p,"abcdef") copies min(len(p),6)=3 bytes, returns 6 -> buf[:6] out of range panic (slice bounds). Test panics -> fail. Fixed returns n=3. Good. But broken `copy(p, "abcdef"); return 6, nil` - copy returns 3 discarded; return 6. Read3 does buf[:6] with len3 -> panic. Good fail.

ex("055_small_iface", "interfaces", "test",
   "Why accept io.Writer instead of *os.File?",
   {"main.go": """// 055: Accept small interfaces, return concrete types. Taking
// io.Writer keeps Write3 usable with buffers, files, network.
// TODO: write exactly "hey" and return its length.
package main

import "io"

func Write3(w io.Writer) (int, error) {
\treturn w.Write([]byte("hello world, this is long"))
}
"""},
   {"main.go": """// 055: Accept small interfaces, return concrete types. Taking
// io.Writer keeps Write3 usable with buffers, files, network.
package main

import "io"

func Write3(w io.Writer) (int, error) {
\treturn w.Write([]byte("hey"))
}
"""},
   {"exercise_test.go": """package main

import (
\t"bytes"
\t"testing"
)

func TestWrite3(t *testing.T) {
\tvar b bytes.Buffer
\tn, err := Write3(&b)
\tif err != nil || n != 3 || b.String() != "hey" {
\t\tt.Fatalf("got %d %q %v", n, b.String(), err)
\t}
}
"""})
# broken writes 25 bytes -> n=25 !=3 -> fail. Good.

print("batch2 done")
