package main

import (
	"fmt"
	"log"
	"os"
	"os/exec"
	"time"
)

// flywheel.go -- repeat a command every delta
func main() {
	argv := os.Args[1:]
	delta := time.Duration(5)
	for {
		out, err := exec.Command(argv[0], argv[1:]...).Output()
		if err != nil {
			log.Fatal(err)
		}
		fmt.Printf("%s", out)
		time.Sleep(time.Second * delta)
	}
}
