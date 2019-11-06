package main

import (
	"errors"
	"fmt"
	"jenkins"
	"net"
	"os"
)

func main() {
	gopath := os.Getenv("GOPATH")
	json := fmt.Sprintf("%s/%s", gopath, "buildctl.json")

	do(json)
}

// do :: string -> IO()
// do invokes jenkins.BuildUser and checks DNS
func do(file string) {
	config := jenkins.LoadConfiguration(file)
	x := jenkins.BuildUser(config)

	if !x.Validated {
		err := errors.New("do")
		jenkins.StepStatus(x, err)
	}

	for _, v := range x.Servers {
		ip, err := net.LookupIP(v)
		jenkins.StepStatus(ip, err)
	}

	jenkins.CallJenkins(x)
	jenkins.StepStatus("Go make a coffee, this takes 15 minutes...")
}
