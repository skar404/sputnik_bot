package sputnik

import (
	"fmt"
	"net/http"
	"strings"
	"time"

	"github.com/skar404/sputnik_bot/global"
	"github.com/skar404/sputnik_bot/requests"
)

var ShortLinkClient = requests.RequestClient{
	Url:     global.SPUTNIK_SHORT_LINK_URL,
	Timeout: 10 * time.Second,
	Header: map[string][]string{
		"Accept-Language": {"en,en-US;q=0.8,ru-RU;q=0.5,ru;q=0.3"},
		"User-Agent":      {"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:85.0) Gecko/20100101 Firefox/85.0"},
	},
}

func GetShortLink(link string) (string, error) {
	s := strings.Split(link, "/")
	if len(s) < 2 {
		return "", fmt.Errorf("not valid url err=%s", link)
	}

	postId := s[len(s)-2]
	if len(postId) < 9 {
		return "", fmt.Errorf("not valid url err=%s", link)
	}
	postId = postId[8:]

	req := requests.Request{
		Method: http.MethodGet,
		Uri:    postId,
		Flags: requests.RequestFlags{
			IsBodyString: true,
		},
	}
	res := requests.Response{}
	err := ShortLinkClient.NewRequest(&req, &res)

	return res.Body, err
}
