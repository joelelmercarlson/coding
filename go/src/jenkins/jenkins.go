package jenkins

import (
	"encoding/json"
	"errors"
	"fmt"
	"github.com/bndr/gojenkins"
	"io/ioutil"
	"log"
	"time"
)

// User :: { User }
// User.URI       = Jenkins API
// User.Username  = Jenkins Auth
// User.Password  = Jenkins Auth
// User.Job       = Jenkins Job
// User.Askid     = askid
// User.Email     = email
// User.Servicenow = servicenow
// User.Servers   = ServerNames to build
// User.Images    = ImageNames for lookup to OperatingSystems
// User.Imagefile = Images.json DB
// User.Delay     = n seconds delay
// User.Retry     = retry count
// User.CallList  = Everything Jenkins Requires
// User.Validated = Sanity checks passed
type User struct {
	URI        string        `json:"uri"`
	Username   string        `json:"username"`
	Password   string        `json:"password"`
	Job        string        `json:"job"`
	Askid      string        `json:"askid"`
	Email      string        `json:"email"`
	Servicenow string        `json:"servicenow"`
	Servers    []string      `json:"servers"`
	Images     []string      `json:"images"`
	Imagefile  string        `json:"imagefile"`
	Parameters []string      `json:"parameters"`
	Delay      time.Duration `json:"delay"`
	Retry      int           `json:"retry"`
	CallList   []map[string]string
	Validated  bool
}

// Images :: { images: [ image ] }
type Images struct {
	Imagelist []Image `json:"images"`
}

// Image :: { image, iso }
type Image struct {
	Image string `json:"image"`
	Iso   string `json:"iso"`
}

// buildCallList :: User, []Paramaters -> []Servers -> []Images -> []map
// buildCallList sets parameters and values
func buildCallList(x User, xs []string, ys []string, zs []string) []map[string]string {
	ms := make([]map[string]string, 0)
	for k := 0; k < len(ys); k++ {
		m := map[string]string{xs[0]: ys[k], xs[1]: zs[k], "Email": x.Email, "Askid": x.Askid, "ServiceNow": x.Servicenow}
		ms = append(ms, m)
	}
	return ms
}

// BuildUser :: User -> User
// BuidlUser sets User.CallList
func BuildUser(x User) User {
	user := x
	images := loadImages(x.Imagefile)
	iso := make([]string, 0)
	for _, v := range x.Images {
		str := imageLookup(images, v)
		if str == "" {
			err := errors.New("invalid image")
			StepStatus(v, err)
		}
		iso = append(iso, str)
	}
	call := buildCallList(user, x.Parameters, x.Servers, iso)
	if len(call) < 1 {
		err := errors.New("invalid Callist")
		StepStatus(x, err)
	}
	user.CallList = call
	user.Validated = true
	return user
}

// CallJenkins :: User -> IO()
// CallJenkins executes concurrent InvokeSimple per CallList
func CallJenkins(x User) {
	jenkins := gojenkins.CreateJenkins(nil, x.URI, x.Username, x.Password)
	_, err := jenkins.Init()
	StepStatus(jenkins.Server, err)

	calls := x.CallList
	c := make(chan int, len(calls))
	for k, _ := range calls {
		m := calls[k]
		go func() {
			build, _ := jenkins.GetJob(x.Job)
			start, err := build.InvokeSimple(m)
			status := fmt.Sprintf("Build :: URI=%s%s Parameters=%v Start=%v", jenkins.Server, build.Base, m, start)
			StepStatus(status, err)

			var ok bool
			for i := 0; i < x.Retry; i++ {
				ok, _ = build.IsRunning()
				if ok {
					i = x.Retry
				}
				time.Sleep(time.Second * x.Delay)
			}
			if !ok {
				err := errors.New("failed to start")
				StepStatus(ok, err)
			}
			c <- 1
		}()
	}
	<-c
}

// imageLookup :: Images -> Image -> Iso
func imageLookup(x Images, y string) string {
	str := ""
	for _, v := range x.Imagelist {
		if y == v.Image {
			str = v.Iso
		}
	}
	return str
}

// LoadConfiguration :: Filename -> User
func LoadConfiguration(x string) User {
	data := User{}
	file, err := ioutil.ReadFile(x)
	StepStatus(x, err)
	_ = json.Unmarshal([]byte(file), &data)
	return data
}

// loadImages :: Filename -> User
func loadImages(x string) Images {
	data := Images{}
	file, err := ioutil.ReadFile(x)
	StepStatus(x, err)
	_ = json.Unmarshal([]byte(file), &data)
	return data
}

// StepStatus :: Message -> error -> IO()
func StepStatus(x interface{}, err ...error) {
	if len(err) > 0 {
		for _, v := range err {
			if v != nil {
				log.Fatal(err)
			}
		}
	}
	log.Println(x)
}
