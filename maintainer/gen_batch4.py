"""Batch 4: stdlib, testing, capstones (082-095)."""
import sys
sys.path.insert(0, ".")
from genlib import add_manifest, write_files

def ex(edir, topic, mode, hint, ex_files, sol_files, test_files=None, expected=None):
    num = edir.split("_")[0]
    add_manifest(num, edir, mode, hint, topic, expected)
    write_files(edir, {"ex": ex_files, "sol": sol_files, "test": test_files})

# ---- stdlib ----
ex("082_json_marshal", "stdlib", "test",
   "Which fields does encoding/json include? What controls key names?",
   {"main.go": """// 082: encoding/json marshals exported fields only. Tags rename keys:
// `json:"name"`. Marshal never fails for simple structs; check errors anyway.
// TODO: produce {"name":"ann","age":3}.
package main

import "encoding/json"

type Person3 struct {
\tName string
\tAge  int
}

func Encode() string {
\tb, err := json.Marshal(Person3{Name: "ann"})
\t_ = err
\treturn string(b)
}
"""},
   {"main.go": """// 082: encoding/json marshals exported fields only. Tags rename keys:
// `json:"name"`. Marshal never fails for simple structs; check errors anyway.
package main

import "encoding/json"

type Person3 struct {
\tName string `json:"name"`
\tAge  int    `json:"age"`
}

func Encode() string {
\tb, err := json.Marshal(Person3{Name: "ann", Age: 3})
\tif err != nil {
\t\treturn ""
\t}
\treturn string(b)
}
"""},
   {"exercise_test.go": """package main

import "testing"

func TestEncode(t *testing.T) {
\tif got := Encode(); got != `{"name":"ann","age":3}` {
\t\tt.Fatalf("got %s", got)
\t}
}
"""})
# broken: missing Age value + uppercase keys -> fails. Good.

ex("083_json_unmarshal", "stdlib", "test",
   "What happens to unknown or missing fields on decode?",
   {"main.go": """// 083: json.Unmarshal matches keys case-insensitively; unknown fields
// are ignored, missing fields keep zero values. Always check the error.
// TODO: decode the payload into a Reading.
package main

import "encoding/json"

type Reading struct {
\tTemp float64 `json:"temp"`
\tUnit string  `json:"unit"`
}

func Decode(s string) (Reading, error) {
\tvar r Reading
\terr := json.Unmarshal([]byte(s), &r)
\tif err != nil {
\t\treturn Reading{}, err
\t}
\tr.Temp = 0
\treturn r, nil
}
"""},
   {"main.go": """// 083: json.Unmarshal matches keys case-insensitively; unknown fields
// are ignored, missing fields keep zero values. Always check the error.
package main

import "encoding/json"

type Reading struct {
\tTemp float64 `json:"temp"`
\tUnit string  `json:"unit"`
}

func Decode(s string) (Reading, error) {
\tvar r Reading
\tif err := json.Unmarshal([]byte(s), &r); err != nil {
\t\treturn Reading{}, err
\t}
\treturn r, nil
}
"""},
   {"exercise_test.go": """package main

import "testing"

func TestDecode(t *testing.T) {
\tr, err := Decode(`{"temp":21.5,"unit":"C"}`)
\tif err != nil || r.Temp != 21.5 || r.Unit != "C" {
\t\tt.Fatalf("got %+v,%v", r, err)
\t}
\tif _, err := Decode(`{bad}`); err == nil {
\t\tt.Fatal("expected error for bad JSON")
\t}
}
"""})
# broken zeroes Temp -> first check fails. Good.

ex("084_http_handler", "stdlib", "test",
   "How do you set the status code and body in a handler?",
   {"main.go": """// 084: net/http handlers take (w http.ResponseWriter, r *http.Request).
// Test them with httptest.NewRecorder without starting a server.
// TODO: answer 200 with exactly "hello".
package main

import "net/http"

func Hello(w http.ResponseWriter, r *http.Request) {
\tw.WriteHeader(http.StatusNotFound)
}
"""},
   {"main.go": """// 084: net/http handlers take (w http.ResponseWriter, r *http.Request).
// Test them with httptest.NewRecorder without starting a server.
package main

import "net/http"

func Hello(w http.ResponseWriter, r *http.Request) {
\tw.WriteHeader(http.StatusOK)
\t_, _ = w.Write([]byte("hello"))
}
"""},
   {"exercise_test.go": """package main

import (
\t"net/http"
\t"net/http/httptest"
\t"testing"
)

func TestHello(t *testing.T) {
\treq := httptest.NewRequest(http.MethodGet, "/", nil)
\trec := httptest.NewRecorder()
\tHello(rec, req)
\tres := rec.Result()
\tif res.StatusCode != http.StatusOK {
\t\tt.Fatalf("got status %d", res.StatusCode)
\t}
\tif rec.Body.String() != "hello" {
\t\tt.Fatalf("got body %q", rec.Body.String())
\t}
}
"""})
# broken: 404 + empty body -> fails. Good.

ex("085_time_format", "stdlib", "test",
   "Why does Go format time with 01-02 15:04:05 instead of %Y-%m-%d?",
   {"main.go": """// 085: Go formats time with the reference layout Mon Jan 2 15:04:05
// MST 2006 (01/02 03:04:05PM '06 -0700). Use time.Date, not strings.
// TODO: format as "2026-01-02".
package main

import "time"

func DayString(t time.Time) string {
\treturn t.Format("02-01-2006")
}
"""},
   {"main.go": """// 085: Go formats time with the reference layout Mon Jan 2 15:04:05
// MST 2006 (01/02 03:04:05PM '06 -0700). Use time.Date, not strings.
package main

import "time"

func DayString(t time.Time) string {
\treturn t.Format("2006-01-02")
}
"""},
   {"exercise_test.go": """package main

import (
\t"testing"
\t"time"
)

func TestDayString(t *testing.T) {
\td := time.Date(2026, 3, 9, 0, 0, 0, 0, time.UTC)
\tif DayString(d) != "2026-03-09" {
\t\tt.Fatalf("got %q", DayString(d))
\t}
}
"""})
# broken "09-03-2026" != want. Good.

ex("086_os_env", "stdlib", "test",
   "How do you read an env var and distinguish unset from empty?",
   {"main.go": """// 086: os.Getenv returns "" for unset AND empty. os.LookupEnv
// returns (value, ok) so you can tell them apart.
// TODO: default to "dev" only when the key is unset.
package main

import "os"

func Env() string {
\tif os.Getenv("APP_ENV") == "" {
\t\treturn "prod"
\t}
\treturn os.Getenv("APP_ENV")
}
"""},
   {"main.go": """// 086: os.Getenv returns "" for unset AND empty. os.LookupEnv
// returns (value, ok) so you can tell them apart.
package main

import "os"

func Env() string {
\tif v, ok := os.LookupEnv("APP_ENV"); ok {
\t\treturn v
\t}
\treturn "dev"
}
"""},
   {"exercise_test.go": """package main

import (
\t"os"
\t"testing"
)

func TestEnv(t *testing.T) {
\tos.Unsetenv("APP_ENV")
\tif Env() != "dev" {
\t\tt.Fatalf("unset should default dev, got %q", Env())
\t}
\tos.Setenv("APP_ENV", "")
\tif Env() != "" {
\t\tt.Fatalf("explicit empty should stay empty, got %q", Env())
\t}
\tos.Setenv("APP_ENV", "prod")
\tif Env() != "prod" {
\t\tt.Fatalf("got %q", Env())
\t}
\tos.Unsetenv("APP_ENV")
}
"""})
# broken: unset -> "prod" (want "dev") fail; explicit empty -> "prod" (want "") fail. Good. Note test uses os pkg; exercise main.go also imports os. Test file package main importing os too - fine.

ex("087_bufio_scan", "stdlib", "test",
   "How do you read a stream line by line? When do you check Err?",
   {"main.go": """// 087: bufio.Scanner splits input (lines by default). Loop with
// Scan(), read with Text(), and check Scanner.Err() afterwards.
// TODO: count the lines.
package main

import (
\t"bufio"
\t"strings"
)

func Lines(s string) int {
\tsc := bufio.NewScanner(strings.NewReader(s))
\tn := 0
\tfor sc.Scan() {
\t\tn += len(sc.Text())
\t}
\treturn n
}
"""},
   {"main.go": """// 087: bufio.Scanner splits input (lines by default). Loop with
// Scan(), read with Text(), and check Scanner.Err() afterwards.
package main

import (
\t"bufio"
\t"strings"
)

func Lines(s string) int {
\tsc := bufio.NewScanner(strings.NewReader(s))
\tn := 0
\tfor sc.Scan() {
\t\tn++
\t}
\treturn n
}
"""},
   {"exercise_test.go": """package main

import "testing"

func TestLines(t *testing.T) {
\tif Lines("ab\\ncde\\nf") != 3 {
\t\tt.Fatalf("got %d", Lines("ab\\ncde\\nf"))
\t}
\tif Lines("") != 0 {
\t\tt.Fatal("empty should be 0")
\t}
}
"""})
# broken sums byte lengths (1+1+1=3 for "a\nb\nc"?) "a"=1,"b"=1,"c"=1 total 3 -> first check PASSES accidentally! Need different test input where char count != line count. Use "ab\ncde\nf": lines=3, chars=2+3+1=6. Change test.

ex("088_flag_slog", "stdlib", "run",
   "How do you declare a flag with a default and parse it?",
   {"main.go": """// 088: The flag package declares CLI options: p := flag.Int(...).
// Call flag.Parse() before use; defaults apply with no args.
// TODO: print "port=8080" using a flag default (no CLI args needed).
package main

import (
\t"flag"
\t"fmt"
)

func main() {
\tport := flag.Int("port", 1234, "port")
\tflag.Parse()
\tfmt.Printf("port=%d\\n", *port)
}
"""},
   {"main.go": """// 088: The flag package declares CLI options: p := flag.Int(...).
// Call flag.Parse() before use; defaults apply with no args.
package main

import (
\t"flag"
\t"fmt"
)

func main() {
\tport := flag.Int("port", 8080, "port")
\tflag.Parse()
\tfmt.Printf("port=%d\\n", *port)
}
"""},
   expected="port=8080")
# broken prints port=1234. Good. Note: flag.Parse in `go run` without args uses default. Good.

ex("089_sort_pkg", "stdlib", "test",
   "When do you reach for sort.Slice vs the slices package?",
   {"main.go": """// 089: sort.Slice sorts with a less func; slices.Sort handles the
// common ordered case. sort is stable only via sort.SliceStable.
// TODO: sort people by age, youngest first.
package main

import "sort"

type Human struct {
\tName string
\tAge  int
}

func ByAge(h []Human) {
\tsort.Slice(h, func(i, j int) bool { return h[i].Age > h[j].Age })
}
"""},
   {"main.go": """// 089: sort.Slice sorts with a less func; slices.Sort handles the
// common ordered case. sort is stable only via sort.SliceStable.
package main

import "sort"

type Human struct {
\tName string
\tAge  int
}

func ByAge(h []Human) {
\tsort.Slice(h, func(i, j int) bool { return h[i].Age < h[j].Age })
}
"""},
   {"exercise_test.go": """package main

import "testing"

func TestByAge(t *testing.T) {
\th := []Human{{"c", 30}, {"a", 20}, {"b", 25}}
\tByAge(h)
\tif h[0].Age != 20 || h[1].Age != 25 || h[2].Age != 30 {
\t\tt.Fatalf("got %+v", h)
\t}
}
"""})
# broken sorts descending -> fail. Good.

# ---- testing ----
ex("090_table_tests", "testing", "test",
   "How do you structure one test func over many cases?",
   {"main.go": """// 090: Table-driven tests loop over (input, want) rows, often with
// subtests via t.Run. One func covers the whole matrix.
// TODO: fix Abs so every row passes.
package main

func Abs(n int) int {
\tif n < 0 {
\t\treturn n
\t}
\treturn n
}
"""},
   {"main.go": """// 090: Table-driven tests loop over (input, want) rows, often with
// subtests via t.Run. One func covers the whole matrix.
package main

func Abs(n int) int {
\tif n < 0 {
\t\treturn -n
\t}
\treturn n
}
"""},
   {"exercise_test.go": """package main

import "testing"

func TestAbs(t *testing.T) {
\tcases := []struct {
\t\tin, want int
\t}{
\t\t{-3, 3}, {0, 0}, {4, 4}, {-100, 100},
\t}
\tfor _, c := range cases {
\t\tt.Run("", func(t *testing.T) {
\t\t\tif got := Abs(c.in); got != c.want {
\t\t\t\tt.Fatalf("Abs(%d)=%d want %d", c.in, got, c.want)
\t\t\t}
\t\t})
\t}
}
"""})
# broken Abs(-3)=-3 -> fail. Good. Note: subtests capture c (1.22 per-iteration, fine).

ex("091_helper_subtests", "testing", "test",
   "What does t.Helper() do for failure lines?",
   {"main.go": """// 091: Helpers shared by tests call t.Helper() so failures point
// at the caller, not inside the helper. Mark cleanup with t.Cleanup.
// TODO: compare with the helper so equal slices pass.
package main

import "testing"

func CheckEqual(t *testing.T, got, want []int) {
\tt.Helper()
\tif len(got) != len(want) {
\t\tt.Fatalf("len %d != %d", len(got), len(want))
\t\treturn
\t}
\tfor i := range got {
\t\tif got[i] != want[i]+1 {
\t\t\tt.Fatalf("index %d: %d != %d", i, got[i], want[i])
\t\t}
\t}
}

func Double2(ns []int) []int {
\tout := make([]int, len(ns))
\tfor i, v := range ns {
\t\tout[i] = v * 2
\t}
\treturn out
}
"""},
   {"main.go": """// 091: Helpers shared by tests call t.Helper() so failures point
// at the caller, not inside the helper. Mark cleanup with t.Cleanup.
package main

import "testing"

func CheckEqual(t *testing.T, got, want []int) {
\tt.Helper()
\tif len(got) != len(want) {
\t\tt.Fatalf("len %d != %d", len(got), len(want))
\t\treturn
\t}
\tfor i := range got {
\t\tif got[i] != want[i] {
\t\t\tt.Fatalf("index %d: %d != %d", i, got[i], want[i])
\t\t}
\t}
}

func Double2(ns []int) []int {
\tout := make([]int, len(ns))
\tfor i, v := range ns {
\t\tout[i] = v * 2
\t}
\treturn out
}
"""},
   {"exercise_test.go": """package main

import "testing"

func TestDouble2(t *testing.T) {
\tCheckEqual(t, Double2([]int{1, 2}), []int{2, 4})
}
"""})
# broken helper compares got[i] != want[i]+1: got [2,4] vs want+1 [3,5] -> fail. Fixed passes. Good. (Teaches helper; fix in helper.)

ex("092_bench_fuzz", "testing", "test",
   "What do benchmarks measure, and what does fuzzing explore?",
   {"main.go": """// 092: Benchmarks (BenchmarkX) time hot paths: `go test -bench=.`.
// Fuzzing (FuzzY) explores inputs: `go test -fuzz=FuzzReverse`.
// TODO: make Reverse actually reverse (both users rely on it).
package main

import "testing"

func Reverse(s string) string {
\tr := []rune(s)
\tfor i, j := 0, len(r)-1; i < j; i, j = i+1, j-1 {
\t\tr[i], r[j] = r[j], r[i]
\t}
\t_ = r
\treturn s
}

var _ = testing.AllocsPerRun

func BenchmarkReverse(b *testing.B) {
\tfor i := 0; i < b.N; i++ {
\t\tReverse("hello world, this is a benchmark")
\t}
}

func FuzzReverse(f *testing.F) {
\tf.Add("hello")
\tf.Fuzz(func(t *testing.T, s string) {
\t\tif Reverse(Reverse(s)) != s {
\t\t\tt.Fatalf("double reverse failed for %q", s)
\t\t}
\t})
}
"""},
   {"main.go": """// 092: Benchmarks (BenchmarkX) time hot paths: `go test -bench=.`.
// Fuzzing (FuzzY) explores inputs: `go test -fuzz=FuzzReverse`.
package main

import "testing"

func Reverse(s string) string {
\tr := []rune(s)
\tfor i, j := 0, len(r)-1; i < j; i, j = i+1, j-1 {
\t\tr[i], r[j] = r[j], r[i]
\t}
\treturn string(r)
}

func BenchmarkReverse(b *testing.B) {
\tfor i := 0; i < b.N; i++ {
\t\tReverse("hello world, this is a benchmark")
\t}
}

func FuzzReverse(f *testing.F) {
\tf.Add("hello")
\tf.Fuzz(func(t *testing.T, s string) {
\t\tif Reverse(Reverse(s)) != s {
\t\t\tt.Fatalf("double reverse failed for %q", s)
\t\t}
\t})
}
"""},
   {"exercise_test.go": """package main

import "testing"

func TestReverse(t *testing.T) {
\tif Reverse("abc") != "cba" {
\t\tt.Fatalf("got %q", Reverse("abc"))
\t}
\tif Reverse("héllo") != "olléh" {
\t\tt.Fatalf("got %q", Reverse("héllo"))
\t}
}
"""})
# broken returns s unchanged -> "abc" != "cba" fail. Fixed reverses runes. Also broken imports? Broken has no imports but uses testing.B/F in Benchmark/Fuzz signatures -> needs `import "testing"`! Broken main.go lacks import -> compile error (undefined testing). That still fails, but solution imports testing. For consistency add import to broken too. Fix: add `import "testing"` to broken.

# ---- capstones (multi-file) ----
ex("093_lru_cache", "capstone", "test",
   "How do a map plus a list give O(1) get, put and eviction?",
   {"cache.go": """// 093: CAPSTONE: an LRU cache pairs a map (lookup) with a list
// (recency). Get promotes; Put evicts the back when over capacity.
// This file plus main.go form one program; the test is the spec.
// TODO: promote hits to the front and evict the least-recently-used.
package main

import "container/list"

type entry struct {
\tkey string
\tval int
}

type LRU struct {
\tcap   int
\titems map[string]*list.Element
\torder *list.List
}

func NewLRU(capacity int) *LRU {
\treturn &LRU{cap: capacity, items: map[string]*list.Element{}, order: list.New()}
}

func (c *LRU) Get(key string) (int, bool) {
\tif el, ok := c.items[key]; ok {
\t\treturn el.Value.(entry).val, true
\t}
\treturn 0, false
}

func (c *LRU) Put(key string, val int) {
\tif el, ok := c.items[key]; ok {
\t\tel.Value = entry{key, val}
\t\treturn
\t}
\tel := c.order.PushFront(entry{key, val})
\tc.items[key] = el
}
""",
    "main.go": """// 093 demo entrypoint (not used by the test).
package main

func demoLRU() {
\tc := NewLRU(2)
\tc.Put("a", 1)
\tc.Put("b", 2)
\t_, _ = c.Get("a")
}
"""},
   {"cache.go": """// 093: CAPSTONE: an LRU cache pairs a map (lookup) with a list
// (recency). Get promotes; Put evicts the back when over capacity.
package main

import "container/list"

type entry struct {
\tkey string
\tval int
}

type LRU struct {
\tcap   int
\titems map[string]*list.Element
\torder *list.List
}

func NewLRU(capacity int) *LRU {
\treturn &LRU{cap: capacity, items: map[string]*list.Element{}, order: list.New()}
}

func (c *LRU) Get(key string) (int, bool) {
\tif el, ok := c.items[key]; ok {
\t\tc.order.MoveToFront(el)
\t\treturn el.Value.(entry).val, true
\t}
\treturn 0, false
}

func (c *LRU) Put(key string, val int) {
\tif el, ok := c.items[key]; ok {
\t\tel.Value = entry{key, val}
\t\tc.order.MoveToFront(el)
\t\treturn
\t}
\tel := c.order.PushFront(entry{key, val})
\tc.items[key] = el
\tfor len(c.items) > c.cap {
\t\tback := c.order.Back()
\t\tif back == nil {
\t\t\tbreak
\t\t}
\t\tc.order.Remove(back)
\t\tdelete(c.items, back.Value.(entry).key)
\t}
}
""",
    "main.go": """// 093 demo entrypoint (not used by the test).
package main

func demoLRU() {
\tc := NewLRU(2)
\tc.Put("a", 1)
\tc.Put("b", 2)
\t_, _ = c.Get("a")
}
"""},
   {"exercise_test.go": """package main

import "testing"

func TestLRU(t *testing.T) {
\tc := NewLRU(2)
\tc.Put("a", 1)
\tc.Put("b", 2)
\tif v, ok := c.Get("a"); !ok || v != 1 {
\t\tt.Fatalf("get a: %v %v", v, ok)
\t}
\tc.Put("c", 3) // evicts b (a was just used)
\tif _, ok := c.Get("b"); ok {
\t\tt.Fatal("b should have been evicted")
\t}
\tif v, ok := c.Get("c"); !ok || v != 3 {
\t\tt.Fatalf("get c: %v %v", v, ok)
\t}
\tc.Put("a", 10)
\tif v, ok := c.Get("a"); !ok || v != 10 {
\t\tt.Fatalf("update a: %v %v", v, ok)
\t}
}
"""})
# broken: no promotion, no eviction -> after Put c, b still present -> "b should have been evicted" fails. Good.

ex("094_url_fetcher", "capstone", "test",
   "How do a semaphore and WaitGroup bound concurrency and collect errors?",
   {"fetch.go": """// 094: CAPSTONE: fetch URLs concurrently with at most `limit`
// in flight (semaphore channel), collecting per-URL errors by hand.
// TODO: bound concurrency, wait for all, and record errors.
package main

import (
\t"io"
\t"net/http"
\t"sync"
)

func FetchAll(urls []string, limit int) map[string]int {
\tout := map[string]int{}
\tvar mu sync.Mutex
\tfor _, u := range urls {
\t\tresp, err := http.Get(u)
\t\tif err != nil {
\t\t\tcontinue
\t\t}
\t\tbody, _ := io.ReadAll(resp.Body)
\t\tresp.Body.Close()
\t\tmu.Lock()
\t\tout[u] = len(body)
\t\tmu.Unlock()
\t}
\treturn out
}

var _ = sync.WaitGroup{}
""",
    "main.go": """// 094 demo entrypoint (not used by the test).
package main

func demoFetch() {
\t_ = FetchAll(nil, 2)
}
"""},
   {"fetch.go": """// 094: CAPSTONE: fetch URLs concurrently with at most `limit`
// in flight (semaphore channel), collecting per-URL errors by hand.
package main

import (
\t"io"
\t"net/http"
\t"sync"
)

func FetchAll(urls []string, limit int) map[string]int {
\tif limit < 1 {
\t\tlimit = 1
\t}
\tout := map[string]int{}
\tvar mu sync.Mutex
\tvar wg sync.WaitGroup
\tsem := make(chan struct{}, limit)
\tfor _, u := range urls {
\t\twg.Add(1)
\t\tsem <- struct{}{}
\t\tgo func(u string) {
\t\t\tdefer wg.Done()
\t\t\tdefer func() { <-sem }()
\t\t\tresp, err := http.Get(u)
\t\t\tif err != nil {
\t\t\t\treturn
\t\t\t}
\t\t\tdefer resp.Body.Close()
\t\t\tbody, _ := io.ReadAll(resp.Body)
\t\t\tmu.Lock()
\t\t\tout[u] = len(body)
\t\t\tmu.Unlock()
\t\t}(u)
\t}
\twg.Wait()
\treturn out
}
""",
    "main.go": """// 094 demo entrypoint (not used by the test).
package main

func demoFetch() {
\t_ = FetchAll(nil, 2)
}
"""},
   {"exercise_test.go": """package main

import (
\t"net/http"
\t"net/http/httptest"
\t"strings"
\t"testing"
\t"time"
)

func TestFetchAll(t *testing.T) {
\tsrv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
\t\ttime.Sleep(60 * time.Millisecond)
\t\t_, _ = w.Write([]byte(strings.Repeat("x", 10)))
\t}))
\tdefer srv.Close()
\turls := []string{srv.URL + "/a", srv.URL + "/b", srv.URL + "/c", srv.URL + "/d"}
\tstart := time.Now()
\tgot := FetchAll(urls, 4)
\tif time.Since(start) > 150*time.Millisecond {
\t\tt.Fatalf("too slow: fetches look sequential (%v)", time.Since(start))
\t}
\tfor _, u := range urls {
\t\tif got[u] != 10 {
\t\t\tt.Fatalf("url %s: got %d want 10", u, got[u])
\t\t}
\t}
}
"""})
# broken sequential: 4x30ms=120ms < 150ms threshold -> might PASS timing! Tighten: sleep 60ms -> sequential 240ms > 150ms; concurrent 60ms < 150ms. Change sleep to 60ms.

ex("095_cli_json", "capstone", "run",
   "How do flags, JSON output and exit codes fit in a tiny CLI?",
   {"greet.go": """// 095: CAPSTONE: a tiny CLI: flags in, JSON out. Keep main thin;
// testable funcs return values, main handles flags/os.Exit.
// TODO: default name to "gopher" and emit valid JSON.
package main

import "fmt"

func Greet(name string) string {
\treturn fmt.Sprintf("hi %s", name)
}
""",
    "main.go": """// 095 main: parse flags, print JSON. (Edit greet.go for the fix.)
package main

import (
\t"flag"
\t"fmt"
)

func main() {
\tname := flag.String("name", "", "who to greet")
\tflag.Parse()
\tif *name == "" {
\t\t*name = "stranger"
\t}
\tfmt.Printf("{\\"greeting\\": \\"%s\\"}\\n", Greet(*name))
}
"""},
   {"greet.go": """// 095: CAPSTONE: a tiny CLI: flags in, JSON out. Keep main thin;
// testable funcs return values, main handles flags/os.Exit.
package main

import "fmt"

func Greet(name string) string {
\treturn fmt.Sprintf("hi %s", name)
}
""",
    "main.go": """// 095 main: parse flags, print JSON.
package main

import (
\t"flag"
\t"fmt"
)

func main() {
\tname := flag.String("name", "gopher", "who to greet")
\tflag.Parse()
\tfmt.Printf("{\\"greeting\\": \\"%s\\"}\\n", Greet(*name))
}
"""},
   expected='{"greeting": "hi gopher"}')
# NOTE: for run mode with extra files we must NOT write exercise_test.go.
# write_files writes test files dict; passing None breaks. Handle: pass test_files=None and
# include main_test.go inside ex/sol file dicts instead. But main_test.go with only package
# clause and comment compiles as test file with no tests: `go vet`? `go test` "no test files"? It's fine since mode=run never runs go test. But `go vet ./...` in CI WILL compile test files across all packages! A _test.go with no Test funcs is fine for vet (it typechecks, reports "no tests to run" only for go test, vet is fine).
# However write_files writes test_files dict into BOTH ex and sol dirs. We want main_test.go placeholder out. Simpler: drop main_test.go entirely; extra file is cli.go + main? We have cli.go containing main() — that's enough (main.go vs cli.go: package main with func main in cli.go compiles for go run). But then exercise dir has single .go file cli.go; spec wants multi-file capstones. 093/094 already multi-file (cache.go+main.go, fetch.go+main.go). For 095, keep cli.go only? The spec example "tiny CLI with flags and JSON output" single file is fine, but "3-5 small multi-file exercises" — make 095 multi-file too: split Greet into greet.go and main into main.go.
# Rework below via fixup: remove main_test.go, use greet.go + main.go.

print("batch4 done")
