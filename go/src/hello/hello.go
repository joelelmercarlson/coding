package main

import (
	"encoding/json"
	"fmt"
	"log"
	"os"
)

type Hello struct {
	Num  float64
	Strs []string
	Str  string
}

func main() {
	byt := []byte(`{"num":1.2345,"strs":["Hello","World","from", "go!"],"str":"hello world"}`)
	dt := &Hello{
		Num:  1.2345,
		Strs: []string{"Hello", "World", "from", "go!"},
		Str:  "hello world",
	}

	// Unmarshal, emulating json to golang
	var dat map[string]interface{}
	if err := json.Unmarshal(byt, &dat); err != nil {
		log.Fatal(err)
	}
	// usual types float64, string, []interface{}
	num := dat["num"].(float64)
	fmt.Println(num)
	str := dat["str"].(string)
	fmt.Println(str)
	strs := dat["strs"].([]interface{})
	fmt.Println(strs)

	// Marshal, emulating struct to json
	dat1, err := json.Marshal(dt)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(dat1)
	enc := json.NewEncoder(os.Stdout)
	enc.Encode(dt)

}
