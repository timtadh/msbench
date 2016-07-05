package main

import (
	"os"
)

import (
	"golang.org/x/tools/go/loader"
	"golang.org/x/tools/go/ssa"
	"golang.org/x/tools/go/ssa/ssautil"
)

import (
	"msbench/examples"
)

const buildmode = ssa.PrintPackages

func main() {
	examples.Main(os.Args[1:], parseGo)
}

func parseGo(pkg string) error {
	var conf loader.Config
	conf.Import(pkg)
	lprog, err := conf.Load()
	if err != nil {
		return err
	}
	_ = ssautil.CreateProgram(lprog, buildmode)
	return nil
}

