package sputnik

import (
	"encoding/xml"
	"fmt"
	"net/http"
	"time"

	"github.com/skar404/sputnik_bot/requests"
)

type Rss struct {
	XMLName xml.Name `xml:"rss"`
	Text    string   `xml:",chardata"`
	Dc      string   `xml:"dc,attr"`
	Atom    string   `xml:"atom,attr"`
	Media   string   `xml:"media,attr"`
	Content string   `xml:"content,attr"`
	Itunes  string   `xml:"itunes,attr"`
	Rambler string   `xml:"rambler,attr"`
	News    string   `xml:"news,attr"`
	Video   string   `xml:"video,attr"`
	Image   string   `xml:"image,attr"`
	Version string   `xml:"version,attr"`
	Channel struct {
		Text        string `xml:",chardata"`
		Title       string `xml:"title"`
		Link        string `xml:"link"`
		Description string `xml:"description"`
		Language    string `xml:"language"`
		Copyright   string `xml:"copyright"`
		Item        []struct {
			Text    string `xml:",chardata"`
			Title   string `xml:"title"`
			Link    string `xml:"link"`
			Guid    string `xml:"guid"`
			Related struct {
				Text    string   `xml:",chardata"`
				Sputnik string   `xml:"sputnik,attr"`
				URL     []string `xml:"url"`
			} `xml:"related"`
			Priority struct {
				Text    string `xml:",chardata"`
				Sputnik string `xml:"sputnik,attr"`
			} `xml:"priority"`
			PubDate     string `xml:"pubDate"`
			Description string `xml:"description"`
			Type        struct {
				Text    string `xml:",chardata"`
				Sputnik string `xml:"sputnik,attr"`
			} `xml:"type"`
			Category  string `xml:"category"`
			Enclosure []struct {
				Text       string `xml:",chardata"`
				Type       string `xml:"type,attr"`
				URL        string `xml:"url,attr"`
				SourceName string `xml:"source_name,attr"`
				Length     string `xml:"length,attr"`
			} `xml:"enclosure"`
		} `xml:"item"`
	} `xml:"channel"`
}

var RssClient = requests.RequestClient{
	Url:     "http://sputniknews.cn/export/rss2/archive/index.xml",
	Timeout: 10 * time.Second,
	Header: map[string][]string{
		"Accept-Language": {"en,en-US;q=0.8,ru-RU;q=0.5,ru;q=0.3"},
		"User-Agent":      {"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:85.0) Gecko/20100101 Firefox/85.0"},
	},
}

func GetRss(r *Rss) error {
	req := requests.Request{Method: http.MethodGet}
	res := requests.Response{}

	if err := RssClient.NewRequest(&req, &res); err != nil || res.Code != 200 {
		if res.Code != 200 {
			return fmt.Errorf("not valid http code: %d", res.Code)
		}
		return fmt.Errorf("error reqeust err=%w", err)
	}

	if err := xml.Unmarshal(res.BodyRaw, &r); err != nil {
		return fmt.Errorf("error parse XML err=%w", err)
	}

	return nil
}
