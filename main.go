package main

import (
	"encoding/xml"
	"fmt"
	"net/http"
	"time"

	"github.com/skar404/sputnik_bok/requests"
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

var SputnikClient = requests.RequestClient{
	Url:     "http://sputniknews.cn/export/rss2/archive/index.xml",
	Timeout: 1 * time.Second,
}

func main() {
	for true {
		rssFeed := Rss{}
		err := Parser(&rssFeed)
		if err != nil {
			fmt.Sprintln(err)
		}

		Notification(&rssFeed)

		time.Sleep(1 * time.Second)
	}
}

func Notification(r *Rss) {
	for i, v := range r.Channel.Item {
		fmt.Println(i, v)
	}
}

func Parser(r *Rss) error {
	req := requests.Request{
		Method: http.MethodGet,
		Uri:    "",
		Flags: requests.RequestFlags{
			IsBodyString: true,
		},
	}
	res := requests.Response{}

	if err := SputnikClient.NewRequest(&req, &res); err != nil || res.Code != 200 {
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
