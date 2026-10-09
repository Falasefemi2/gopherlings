// 042: Embedding composes behavior: outer structs promote the
// embedded type's methods. No inheritance, just composition.
// TODO: make Logger available on Server via embedding.
package main

type Logger struct{}

func (Logger) Log(s string) string { return "log:" + s }

type Server struct {
	*Logger
	Name string
}

func NewServer() *Server {
	return &Server{Name: "web", Logger: &Logger{}}
}
