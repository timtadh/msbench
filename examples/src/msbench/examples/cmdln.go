package examples

import (
	"fmt"
	"log"
	"os"
	"os/signal"
	"runtime/debug"
	"runtime/pprof"
	"strconv"
	"syscall"
)

import (
	"github.com/timtadh/getopt"
)


func Main(argv []string, f func(path string) error) {
	args, optargs, err := getopt.GetOpt(
		argv,
		"p:l:",
		[]string{"cpu-profile=", "loops="},
	)
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(-1)
	}
	cpuProfile := ""
	loops := 1
	for _, oa := range optargs {
		switch oa.Opt() {
		case "-p", "--cpu-profile":
			cpuProfile = oa.Arg()
		case "-l", "--loops":
			loops, err = strconv.Atoi(oa.Arg())
			if err != nil {
				log.Printf("expected an int for -l,--loop got %v", oa.Arg())
				log.Println(err)
				os.Exit(-1)
			}
		}
	}
	cleanup := func() {}
	if cpuProfile != "" {
		cleanup = CPUProfile(cpuProfile)
	}
	run(loops, args, f, cleanup)
}

func run(loops int, paths []string, f func(path string) error, cleanup func()) {
	exitCode := 0
	defer func() {
		if e := recover(); e != nil {
			log.Println(e)
			debug.PrintStack()
			exitCode++
		}
		cleanup()
		os.Exit(exitCode)
	}()
pathLoop:
	for _, path := range paths {
		for i := 0; i < loops; i++ {
			err := f(path)
			if err != nil {
				log.Printf("err for %v: %v", path, err)
				exitCode++
				continue pathLoop
			}
		}
	}
}

func CPUProfile(output string) func() {
	f, err := os.Create(output)
	if err != nil {
		log.Fatal(err)
	}
	err = pprof.StartCPUProfile(f)
	if err != nil {
		log.Fatal(err)
	}
	sigs := make(chan os.Signal, 1)
	signal.Notify(sigs, syscall.SIGINT, syscall.SIGTERM)
	go func() {
		sig:=<-sigs
		pprof.StopCPUProfile()
		f.Close()
		panic(fmt.Errorf("caught signal: %v", sig))
	}()
	return func() {
		pprof.StopCPUProfile()
		f.Close()
	}
}

