# dir
GOPATH := $(HOME)/go
BIN := $(GOPATH)/bin
SRC := $(GOPATH)/src
TMP := /tmp
VAR := /var
VARTMP := $(VAR)$(TMP)

# tools
CURL  := /usr/bin/curl
UNAME := $(shell uname -s|tr 'A-Z' 'a-z')
GODL  := $(shell printf "https://dl.google.com/go/go1.13.6.%s-amd64.tar.gz" $(UNAME))

# git
GIT     := git
GITDIFF := $(GIT) diff
GITLOG  := $(GIT) log
GITPULL := $(GIT) pull
GITSTATUS := $(GIT) status

# go
GO        := go
GOBUILD   := $(GO) build
GODOC     := godoc
GOLINT    := golint
GOCLEAN   := $(GO) clean
GOGET     := $(GO) get
GOINSTALL := $(GO) install
GOLIST    := $(GO) list
GOTEST    := $(GO) test

# tools
COMMIT   := $(BIN)/commit
FLYWHEEL := $(bin)/flywheel
GORE     := $(BIN)/gore
OOO      := $(BIN)/ooo

all: emacs gore libraries
.PHONY: all

buildctl: pull
	$(GOINSTALL) buildctl
	$(BIN)/buildctl

clean:
	$(GOCLEAN)

commit:
	$(COMMIT)

diff:
	$(GITDIFF)

emacs:
	$(GOGET) github.com/nsf/gocode
	$(GOGET) github.com/rogpeppe/godef
	$(GOGET) golang.org/x/tools/cmd/guru
	$(GOGET) golang.org/x/tools/cmd/gorename
	$(GOGET) golang.org/x/tools/cmd/goimports
	$(GOGET) golang.org/x/tools/cmd/godoc

download:
	cd $(VARTMP) ; $(CURL) -O $(GODL)

gore:
	GO11MODULE=off $(GOGET) golang.org/x/lint/golint
	GO111MODULE=off $(GOGET) github.com/motemen/gore/cmd/gore

immutable: pull
	$(GOINSTALL) immutable
	$(BIN)/immutable

libraries:
	$(GOGET) github.com/bndr/gojenkins
	$(GOGET) github.com/calbucci/go-htmlparser

log:
	$(GITLOG)

pull:
	$(GITPULL)

run:
	@echo "make godl"
	@echo "make all"
	@echo "cat <<EOF > hello.go"
	@echo "package main"
	@echo "import \"fmt\""
	@echo "func main() { fmt.Println(\"Hello World\") }"
	@echo "EOF"
	@echo "go run hello.go"

status:
	$(GITSTATUS)

tools:
	$(GOINSTALL) commit
	$(GOINSTALL) ooo
	$(GOINSTALL) flywheel
