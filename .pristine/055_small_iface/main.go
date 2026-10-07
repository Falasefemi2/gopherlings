// 055: Accept small interfaces, return concrete types. Taking
// io.Writer keeps Write3 usable with buffers, files, network.
// TODO: write exactly "hey" and return its length.
package main

import "io"

func Write3(w io.Writer) (int, error) {
	return w.Write([]byte("hello world, this is long"))
}
