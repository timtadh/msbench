package main

import (
	"os"
)

import (
	"golang.org/x/net/html"
)

import (
	"msbench/examples"
)


func main() {
	examples.Main(os.Args[1:], parseHtml)
}

func parseHtml(path string) error {
	f, err := os.Open(path)
	if err != nil {
		return err
	}
	_, err = html.Parse(f)
	if err != nil {
		return err
	}
	return f.Close()
}
