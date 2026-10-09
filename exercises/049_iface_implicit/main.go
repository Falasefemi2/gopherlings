// 049: Interfaces are satisfied implicitly: no `implements` keyword.
// A type satisfies Greeter by having Greet() string with that signature.
// TODO: give Loud a Greet method so it satisfies Greeter.
package main

type Greeter interface{ Greet() string }

type Loud struct{ Who string }

func Shout(g Greeter) string { return g.Greet() + "!" }

func (l Loud) Greet() string {
	return "hi " + l.Who
}

func Call() string { return Shout(Loud{Who: "bob"}) }
