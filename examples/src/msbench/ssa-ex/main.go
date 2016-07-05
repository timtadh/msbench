package main

import (
	"os"
)

import (
	"golang.org/x/tools/go/loader"
	"golang.org/x/tools/go/ssa"
	"golang.org/x/tools/go/ssa/ssautil"
	"golang.org/x/tools/go/callgraph/rta"
)

import (
	"msbench/examples"
)

const buildmode = 0

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
	program := ssautil.CreateProgram(lprog, buildmode)
	program.Build()
	var mains []*ssa.Function
	for _, pkg := range program.AllPackages() {
		mainFunc := pkg.Func("main")
		if mainFunc != nil {
			mains = append(mains, mainFunc)
		}
	}
	if len(mains) > 0 {
		rta.Analyze(mains, true)
	}
	return nil
}

