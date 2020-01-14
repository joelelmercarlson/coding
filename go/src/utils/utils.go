package utils

import (
	"crypto/md5"
	"fmt"
	"io"
	"io/ioutil"
	"log"
	"net/http"
	"os"
)

// CreateFile -- create a file with mode 0644
func CreateFile(x []byte, y string) error {
	err := ioutil.WriteFile(y, x, 0644)
	if err != nil {
		return err
	}
	return nil
}

// GetContents -- writes output to a file in small chunks
func GetContents(x string, y string) error {
	out, err := os.Create(y)
	if err != nil {
		return err
	}
	defer out.Close()

	resp, err := http.Get(x)
	if err != nil {
		return err
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return fmt.Errorf("bad status: %s", resp.Status)
	}

	_, err = io.Copy(out, resp.Body)
	if err != nil {
		return err
	}
	return nil
}

// GetRepo -- GetContents, ReadFile, return string
func GetRepo(x string, y string) string {
	err := GetContents(x, y)
	if err != nil {
		log.Fatal(err)
	}
	data, err := ioutil.ReadFile(y)
	if err != nil {
		log.Fatal(err)
	}
	return string(data)
}

// GetSize -- size of file
func GetSize(x string) int64 {
	st, err := os.Stat(x)
	if err != nil {
		return 0
	}
	return st.Size()
}

func hashBytes(x []byte) [16]byte {
	return md5.Sum(x)
}

// HashFile -- md5sum of a file
func HashFile(x string) [16]byte {
	var i [16]byte
	data, err := ioutil.ReadFile(x)
	if err != nil {
		return i
	}
	return hashBytes(data)
}
