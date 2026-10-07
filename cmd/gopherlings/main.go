// Command gopherlings runs the Gopherlings exercises in order,
// stopping at the first failure. See README.md for usage.
package main

import (
	"bytes"
	"encoding/json"
	"flag"
	"fmt"
	"io"
	"io/fs"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
	"time"
)

type Exercise struct {
	ID             string `json:"id"`
	Dir            string `json:"dir"`
	Mode           string `json:"mode"` // "run" | "test"
	ExpectedOutput string `json:"expectedOutput,omitempty"`
	Hint           string `json:"hint"`
	Topic          string `json:"topic"`
}

var (
	useColor = os.Getenv("NO_COLOR") == "" && os.Getenv("TERM") != "dumb"
)

func color(code, s string) string {
	if !useColor {
		return s
	}
	return "\x1b[" + code + "m" + s + "\x1b[0m"
}

func green(s string) string  { return color("32", s) }
func red(s string) string    { return color("31", s) }
func yellow(s string) string { return color("33", s) }
func cyan(s string) string   { return color("36", s) }
func bold(s string) string   { return color("1", s) }

func findRoot() string {
	// 1. cwd
	if cwd, err := os.Getwd(); err == nil {
		for d := cwd; ; d = filepath.Dir(d) {
			if _, err := os.Stat(filepath.Join(d, "exercises.json")); err == nil {
				return d
			}
			parent := filepath.Dir(d)
			if parent == d {
				break
			}
		}
	}
	// 2. executable location
	if exe, err := os.Executable(); err == nil {
		d := filepath.Dir(exe)
		for i := 0; i < 6; i++ {
			if _, err := os.Stat(filepath.Join(d, "exercises.json")); err == nil {
				return d
			}
			d = filepath.Dir(d)
		}
	}
	// fallback: cwd
	cwd, _ := os.Getwd()
	return cwd
}

func loadManifest(root string) ([]Exercise, error) {
	data, err := os.ReadFile(filepath.Join(root, "exercises.json"))
	if err != nil {
		return nil, err
	}
	var exs []Exercise
	if err := json.Unmarshal(data, &exs); err != nil {
		return nil, err
	}
	return exs, nil
}

type result struct {
	ok     bool
	output string
}

func runExercise(root string, ex Exercise) result {
	rel := "./" + filepath.ToSlash(filepath.Join("exercises", ex.Dir))
	var cmd *exec.Cmd
	if ex.Mode == "test" {
		cmd = exec.Command("go", "test", "-count=1", rel)
	} else {
		cmd = exec.Command("go", "run", rel)
	}
	cmd.Dir = root
	cmd.Env = append(os.Environ(), "NO_COLOR=1")
	var buf bytes.Buffer
	cmd.Stdout = &buf
	cmd.Stderr = &buf
	err := cmd.Run()
	out := buf.String()
	if err != nil {
		return result{false, out}
	}
	if ex.Mode == "run" && ex.ExpectedOutput != "" {
		got := strings.TrimSpace(out)
		want := strings.TrimSpace(ex.ExpectedOutput)
		if got != want {
			msg := fmt.Sprintf("wrong output.\n--- got ---\n%s\n--- want ---\n%s\n", got, want)
			return result{false, msg + out}
		}
	}
	return result{true, out}
}

func runSolution(root string, ex Exercise) result {
	rel := "./" + filepath.ToSlash(filepath.Join("solutions", ex.Dir))
	var cmd *exec.Cmd
	if ex.Mode == "test" {
		cmd = exec.Command("go", "test", "-count=1", rel)
	} else {
		cmd = exec.Command("go", "run", rel)
	}
	cmd.Dir = root
	cmd.Env = append(os.Environ(), "NO_COLOR=1")
	var buf bytes.Buffer
	cmd.Stdout = &buf
	cmd.Stderr = &buf
	err := cmd.Run()
	out := buf.String()
	if err != nil {
		return result{false, out}
	}
	if ex.Mode == "run" && ex.ExpectedOutput != "" {
		got := strings.TrimSpace(out)
		want := strings.TrimSpace(ex.ExpectedOutput)
		if got != want {
			return result{false, fmt.Sprintf("wrong output.\n--- got ---\n%s\n--- want ---\n%s\n", got, want)}
		}
	}
	return result{true, out}
}

func findExercise(exs []Exercise, q string) *Exercise {
	q = strings.TrimSpace(q)
	for i := range exs {
		if exs[i].ID == q || exs[i].Dir == q {
			return &exs[i]
		}
		// allow "12" to match "012_..."
		if strings.HasPrefix(exs[i].Dir, q+"_") || strings.HasPrefix(exs[i].ID, q) {
			return &exs[i]
		}
		// allow numeric match ignoring leading zeros
		if strings.TrimLeft(q, "0") != "" {
			if strings.TrimLeft(exs[i].ID, "0") == strings.TrimLeft(q, "0") {
				return &exs[i]
			}
		}
	}
	return nil
}

func printFail(root string, idx int, total int, ex Exercise, res result, showHint bool) {
	fmt.Printf("%s Exercise %s\n", red("✘"), bold(fmt.Sprintf("[%d/%d] %s", idx+1, total, filepath.Join("exercises", ex.Dir))))
	fmt.Printf("  mode: %s  topic: %s\n\n", ex.Mode, ex.Topic)
	out := strings.TrimRight(res.output, "\n")
	if out != "" {
		fmt.Println(out)
		fmt.Println()
	}
	if showHint {
		fmt.Printf("%s %s\n\n", yellow("Hint:"), ex.Hint)
	} else {
		fmt.Printf("Run with %s to see a hint.\n\n", cyan("--hint"))
	}
	// Point at the file to open.
	files := []string{"main.go", "solution.go", "exercise.go", "main_test.go"}
	_ = files
	entries, err := os.ReadDir(filepath.Join(root, "exercises", ex.Dir))
	if err == nil {
		for _, e := range entries {
			if strings.HasSuffix(e.Name(), ".go") && !strings.HasSuffix(e.Name(), "_test.go") {
				fmt.Printf("Open %s and fix it, then re-run.\n", filepath.Join("exercises", ex.Dir, e.Name()))
				return
			}
		}
	}
	fmt.Printf("Open %s and fix it, then re-run.\n", filepath.Join("exercises", ex.Dir))
}

func doRun(root string, exs []Exercise, showHint bool, only string) int {
	if only != "" {
		ex := findExercise(exs, only)
		if ex == nil {
			fmt.Printf("Unknown exercise %q. Use --list to see all.\n", only)
			return 2
		}
		idx := 0
		for i := range exs {
			if exs[i].Dir == ex.Dir {
				idx = i
				break
			}
		}
		res := runExercise(root, *ex)
		if res.ok {
			fmt.Printf("%s [%d/%d] %s passed.\n", green("✔"), idx+1, len(exs), filepath.Join("exercises", ex.Dir))
			return 0
		}
		printFail(root, idx, len(exs), *ex, res, true)
		return 1
	}
	for i, ex := range exs {
		res := runExercise(root, ex)
		if !res.ok {
			printFail(root, i, len(exs), ex, res, showHint)
			return 1
		}
	}
	fmt.Printf("%s All %d exercises pass. You are done!\n", green("✔"), len(exs))
	return 0
}

func doList(root string, exs []Exercise) int {
	// Derive status by actually running.
	for i, ex := range exs {
		res := runExercise(root, ex)
		mark := green("✔")
		state := "done"
		if !res.ok {
			// first failure and everything after is pending except distinguish?
			// To keep it cheap and truthful, mark this one as failing and rest as pending
			// without running them. But spec says derive by running; we run up to first fail,
			// then mark rest pending. That is still derived, not from a state file.
			fmt.Printf("%s [%d/%d] %s  %s\n", red("✘"), i+1, len(exs), ex.Dir, ex.Topic)
			for j := i + 1; j < len(exs); j++ {
				fmt.Printf("%s [%d/%d] %s  %s\n", yellow("○"), j+1, len(exs), exs[j].Dir, exs[j].Topic)
			}
			_ = mark
			_ = state
			return 1
		}
		fmt.Printf("%s [%d/%d] %s  %s\n", mark, i+1, len(exs), ex.Dir, ex.Topic)
	}
	return 0
}

func doReset(root, q string) int {
	if q == "" {
		fmt.Println("Usage: --reset N (exercise id or dir). Example: --reset 12")
		return 2
	}
	exs, err := loadManifest(root)
	if err != nil {
		fmt.Println("cannot load manifest:", err)
		return 2
	}
	ex := findExercise(exs, q)
	if ex == nil {
		fmt.Printf("Unknown exercise %q.\n", q)
		return 2
	}
	srcDir := filepath.Join(root, ".pristine", ex.Dir)
	dstDir := filepath.Join(root, "exercises", ex.Dir)
	entries, err := os.ReadDir(srcDir)
	if err != nil {
		fmt.Printf("No pristine copy for %s: %v\n", ex.Dir, err)
		return 2
	}
	for _, e := range entries {
		if e.IsDir() {
			continue
		}
		src := filepath.Join(srcDir, e.Name())
		dst := filepath.Join(dstDir, e.Name())
		data, err := os.ReadFile(src)
		if err != nil {
			fmt.Println("reset failed:", err)
			return 1
		}
		if err := os.WriteFile(dst, data, 0644); err != nil {
			fmt.Println("reset failed:", err)
			return 1
		}
		fmt.Printf("Reset %s\n", filepath.Join("exercises", ex.Dir, e.Name()))
	}
	return 0
}

func doVerify(root string, exs []Exercise) int {
	failures := 0
	for i, ex := range exs {
		sol := runSolution(root, ex)
		cur := runExercise(root, ex)
		solOK := sol.ok
		curFails := !cur.ok
		status := ""
		if solOK && curFails {
			status = green("OK")
		} else {
			status = red("FAIL")
			failures++
		}
		fmt.Printf("%s [%d/%d] %s mode=%s solution_pass=%v exercise_fails=%v\n",
			status, i+1, len(exs), ex.Dir, ex.Mode, solOK, curFails)
		if !solOK {
			fmt.Printf("  solution output:\n%s\n", indent(sol.output))
		}
		if !curFails {
			fmt.Printf("  WARNING: exercise currently passes; it must fail before the fix.\n")
		}
	}
	if failures > 0 {
		fmt.Printf("\n%s %d/%d exercises need attention.\n", red("FAIL:"), failures, len(exs))
		return 1
	}
	fmt.Printf("\n%s All %d exercises verified: solutions pass, exercises fail.\n", green("PASS:"), len(exs))
	return 0
}

func indent(s string) string {
	lines := strings.Split(strings.TrimRight(s, "\n"), "\n")
	for i, l := range lines {
		lines[i] = "    " + l
	}
	return strings.Join(lines, "\n")
}

func collectMtimes(root string) (map[string]time.Time, error) {
	out := map[string]time.Time{}
	err := filepath.WalkDir(filepath.Join(root, "exercises"), func(p string, d fs.DirEntry, err error) error {
		if err != nil {
			return nil
		}
		if !d.IsDir() && strings.HasSuffix(p, ".go") {
			if st, err := os.Stat(p); err == nil {
				out[p] = st.ModTime()
			}
		}
		return nil
	})
	return out, err
}

func doWatch(root string, exs []Exercise, showHint bool) int {
	fmt.Printf("Watching %s for changes (poll 500ms). Ctrl+C to stop.\n", filepath.Join("exercises"))
	last, _ := collectMtimes(root)
	// initial run
	doRun(root, exs, showHint, "")
	for {
		time.Sleep(500 * time.Millisecond)
		cur, _ := collectMtimes(root)
		changed := false
		if len(cur) != len(last) {
			changed = true
		} else {
			for k, v := range cur {
				if old, ok := last[k]; !ok || !old.Equal(v) {
					changed = true
					break
				}
			}
		}
		if changed {
			fmt.Println(cyan("\n— change detected, re-running —"))
			// reload manifest in case it changed
			if fresh, err := loadManifest(root); err == nil {
				exs = fresh
			}
			doRun(root, exs, showHint, "")
			last = cur
		}
	}
}

func main() {
	var (
		fWatch  = flag.Bool("watch", false, "re-run on file change by polling mtimes")
		fHint   = flag.Bool("hint", false, "show hint for the failing exercise")
		fList   = flag.Bool("list", false, "list all exercises with status")
		fOnly   = flag.String("only", "", "run only exercise N (id or dir)")
		fReset  = flag.String("reset", "", "restore exercise N from .pristine/")
		fVerify = flag.Bool("verify-solutions", false, "check every solution passes and every exercise fails")
		fHelp   = flag.Bool("help", false, "show help")
	)
	flag.BoolVar(fHelp, "h", false, "show help")
	flag.Parse()

	root := findRoot()
	exs, err := loadManifest(root)
	if err != nil {
		fmt.Fprintf(os.Stderr, "cannot load exercises.json (looked from %s): %v\n", root, err)
		os.Exit(2)
	}

	if *fHelp {
		fmt.Println("gopherlings - fix the broken Go programs in order.")
		fmt.Println()
		fmt.Println("Usage:")
		fmt.Println("  go run ./cmd/gopherlings [--hint] [--only N] [--list] [--watch] [--reset N] [--verify-solutions]")
		fmt.Println()
		flag.PrintDefaults()
		return
	}
	if *fReset != "" {
		os.Exit(doReset(root, *fReset))
	}
	if *fVerify {
		os.Exit(doVerify(root, exs))
	}
	if *fList {
		os.Exit(doList(root, exs))
	}
	if *fWatch {
		os.Exit(doWatch(root, exs, *fHint))
	}
	// --hint without other flags: show hint for current failure.
	// --only with --hint also works via doRun.
	if flag.NArg() == 1 && *fOnly == "" {
		// allow positional: go run ./cmd/gopherlings 12
		*fOnly = flag.Arg(0)
	}
	// Copy hint template files? no.
	_, _ = io.Discard, fs.ValidPath
	os.Exit(doRun(root, exs, *fHint, *fOnly))
}
