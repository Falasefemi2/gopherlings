// 054: io.Reader is Read(p []byte) (n int, err error). It returns
// io.EOF at the end; n tells how many bytes were filled.
// TODO: read at most 3 bytes and report n.
package main

import "io"

type Three struct{}

func (Three) Read(p []byte) (int, error) {
	copy(p, "abcdef")
	return 6, nil
}

func Read3(r io.Reader) (string, error) {
	buf := make([]byte, 3)
	n, err := r.Read(buf)
	return string(buf[:n]), err
}
