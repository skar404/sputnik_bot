package weibo

import (
	"bufio"
	"encoding/base64"
	"encoding/json"
	"fmt"
	"io"
	"io/ioutil"
	"log"
	"math"
	"math/rand"
	"net/http"
	"net/url"
	"os"
	"strconv"
	"strings"
	"time"
)

type Config struct {
	Timeout time.Duration

	WeiboUrl string
	SinaUrl  string

	login    string
	password string

	cookies string
}

type Login struct {
	RetCode    int    `json:"retcode"`
	ServerTime int    `json:"servertime"`
	PcId       string `json:"pcid"`
	Nonce      string `json:"nonce"`
	PublicKey  string `json:"pubkey"`
	RsaKv      string `json:"rsakv"`
	IsOpenLock int    `json:"is_openlock"`
	SmsUrl     string `json:"smsurl"`
	ShowPin    int    `json:"showpin"`
	ExecTime   int    `json:"exectime"`
}

func NewConfig() *Config {
	return &Config{
		Timeout:  30 * time.Second,
		WeiboUrl: "https://www.weibo.com/",
		SinaUrl:  "http://login.sina.com.cn/",
	}
}

func stringToBase64(data string) string {
	return base64.StdEncoding.EncodeToString([]byte(data))
}

// Login
// TODO refactoring
//   пока для переоса логики пишу лапшу
//   передавать куку между запросами
func (c *Config) Login(login string, password string) {
	c.login = login
	c.password = password

	client := &http.Client{
		Timeout: c.Timeout,
	}

	req, err := http.NewRequest("GET", c.WeiboUrl+"login.php", nil)
	if err != nil {
		// TODO return correct error
		return
	}

	resp, err := client.Do(req)
	if err != nil {
		// TODO return correct error
		return
	}

	// базовый запрос для получения ключа для логина
	req, err = http.NewRequest("GET", c.SinaUrl+"sso/prelogin.php", nil)
	if err != nil {
		// TODO return correct error
		return
	}

	// параметры для запросы
	loginBase64 := stringToBase64(login)
	timeStamp := string(time.Now().UnixNano() / int64(math.Pow(10, 6)))

	q := req.URL.Query()
	q.Add("entry", "weibo")
	q.Add("callback", "sinaSSOController.preloginCallBack")
	q.Add("su", loginBase64)
	q.Add("rsakt", "mod")
	q.Add("checkpin", "1")
	q.Add("client", "ssologin.js(v1.4.18)")
	q.Add("pre_url", timeStamp)
	req.URL.RawQuery = q.Encode()
	req.Header = resp.Header
	fmt.Println(req.URL.String())

	resp, err = client.Do(req)
	if err != nil {
		// TODO return correct error
		return
	}

	defer resp.Body.Close()
	respBody, _ := ioutil.ReadAll(resp.Body)

	// api отдает данный формата и так избавляемся от лишнего:
	// sinaSSOController.preloginCallBack({валидный json})
	body := string(respBody)
	body = strings.Replace(body, "sinaSSOController.preloginCallBack", "", 1)
	body = strings.Replace(body, "(", "", 1)
	body = strings.Replace(body, ")", "", 1)

	// TODO test data
	fmt.Println(resp.Status)
	fmt.Println(body)

	loginReq := Login{}
	jsonErr := json.Unmarshal([]byte(body), &loginReq)
	if jsonErr != nil {
		// TODO return correct error
		return
	}

	// Получаем капчу
	req, err = http.NewRequest("GET", c.SinaUrl+"cgi/pin.php", nil)
	if err != nil {
		// TODO return correct error
		return
	}

	// случаный числа для запроса на капчу
	min := 10000000
	max := 99999999
	randomString := strconv.Itoa(rand.Intn(max-min+1) + min)

	q = req.URL.Query()
	q.Add("r", randomString)
	q.Add("s", "0")
	q.Add("p", loginReq.PcId)
	req.URL.RawQuery = q.Encode()
	req.Header = resp.Header
	fmt.Println(req.URL.String())

	client = &http.Client{
		Timeout: c.Timeout,
	}

	resp, err = client.Do(req)
	if err != nil {
		// TODO return correct error
		return
	}

	defer resp.Body.Close()
	//respBody, _ = ioutil.ReadAll(resp.Body)

	file, err := os.Create("output.png")
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()
	_, err = io.Copy(file, resp.Body)
	if err != nil {
		log.Fatal(err)
	}

	reader := bufio.NewReader(os.Stdin)
	fmt.Print("Enter captcha: ")
	captcha, _ := reader.ReadString('\n')

	// Логинемся c кукой
	d := url.Values{}
	d.Set("door", captcha)
	d.Set("entry", "weibo")
	d.Set("gateway", "1")
	d.Set("from", "")
	d.Set("savestate", "7")
	d.Set("useticket", "1")
	d.Set("pagerefer", "http://login.sina.com.cn/sso/logout.php?entry=miniblog&r=http%3A%2F%2Fweibo.com%2Flogout.php%3Fbackurl")
	d.Set("vsnf", "1")
	d.Set("su", loginBase64)
	d.Set("service", "miniblog")
	d.Set("servertime", strconv.Itoa(loginReq.ServerTime))
	d.Set("nonce", loginReq.Nonce)
	d.Set("pwencode", "rsa2")
	d.Set("rsakv", loginReq.RsaKv)
	d.Set("sp", password)
	d.Set("sr", "1366*768")
	d.Set("encoding", "UTF-8")
	d.Set("prelt", "115")
	d.Set("url", "http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack")
	d.Set("returntype", "META")

	req, err = http.NewRequest("POST", c.SinaUrl+"sso/login.php?client=ssologin.js(v1.4.18)", strings.NewReader(d.Encode()))
	if err != nil {
		// TODO return correct error
		return
	}
	req.Header = resp.Header

	client = &http.Client{
		Timeout: c.Timeout,
	}
	resp, _ = client.Do(req)
	defer resp.Body.Close()
	respBody, _ = ioutil.ReadAll(resp.Body)

	// api отдает данный формата и так избавляемся от лишнего:
	// sinaSSOController.preloginCallBack({валидный json})
	fmt.Println(string(respBody))

	// Проверяем что мы пошли

	req, err = http.NewRequest("GET", "https://login.sina.com.cn/signup/signin.php?entry=sso", nil)
	if err != nil {
		// TODO return correct error
		return
	}
	req.Header = resp.Header
	resp, _ = client.Do(req)
	respBody, _ = ioutil.ReadAll(resp.Body)
	fmt.Println(string(respBody))
}
