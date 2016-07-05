package main

import (
	"os"
)

import (
	"golang.org/x/debug/elf"
)

import (
	"msbench/examples"
)


func main() {
	examples.Main(os.Args[1:], parseElf)
}

func parseElf(path string) error {
	f, err := elf.Open(path)
	if err != nil {
		return err
	}
	err = process(f)
	if err != nil {
		return err
	}
	return f.Close()
}

func process(f *elf.File) (err error) {
	_, err = f.ImportedLibraries()
	if err != nil {
		return err
	}
	_, err = f.Symbols()
	if err != nil {
		return err
	}
	d, err := f.DWARF()
	if err != nil {
		return err
	}
	r := d.Reader()
	e, err := r.Next()
	if err != nil {
		return err
	}
	for e != nil {
		e, err = r.Next()
		if err != nil {
			return err
		}
	}
	return nil
}

