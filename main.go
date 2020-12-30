package main

import (
	"context"
	"encoding/xml"
	"fmt"
	"net/http"
	"strings"
	"time"

	"github.com/go-redis/redis/v8"

	"github.com/skar404/sputnik_bok/global"
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
	Timeout: 10 * time.Second,
}

var TelegramClient = requests.RequestClient{
	Url:     fmt.Sprintf("https://api.telegram.org/bot%s/", global.TG_TOKEN),
	Timeout: 10 * time.Second,
	Header: map[string][]string{
		"Content-Type": {"application/json"},
		"charset":      {"utf-8"},
	},
}

var SputnikShortLinkClient = requests.RequestClient{
	Url:     global.SPUTNIK_SHORT_LINK_URL,
	Timeout: 10 * time.Second,
}

var DB = redis.NewClient(&redis.Options{
	Addr:     "localhost:6370",
	Password: "", // no password set
	DB:       0,  // use default DB
})

var UniqLink []string

type TgPost struct {
	Message   string
	Link      string
	ShortLink string
	Img       string
}

type sendMessageReq struct {
	ChatId int    `json:"chat_id"`
	Mode   string `json:"parse_mode"`
	Text   string `json:"text,omitempty"`

	Caption string `json:"caption,omitempty"`
	Photo   string `json:"photo,omitempty"`
}

func main() {
	for true {
		rssFeed := Rss{}
		err := GetRss(&rssFeed)
		if err != nil {
			fmt.Sprintln(err)
		}
		Notification(&rssFeed)

		time.Sleep(1 * time.Second)
	}
}

func Notification(r *Rss) {
	for _, v := range r.Channel.Item {
		ctx := context.Background()
		if v.Link == "" {
			fmt.Println(fmt.Sprintf("error get short item=%+v", v))
			continue
		}

		val, err := DB.Get(ctx, v.Link).Result()
		if err == redis.Nil {
			fmt.Printf("new post link=%s\n", v.Link)
		} else if err != nil {
			fmt.Printf("redis is err=%s\n", err)
			continue
		}

		if val != "" {
			continue
		}

		linkShort, err := GetShortLink(v.Link)
		if err != nil {
			fmt.Println(fmt.Sprintf("error get short link err=%s", err))
		}

		link := v.Link
		if linkShort != "" {
			link = linkShort
		}

		img := ""
		if len(v.Enclosure) > 0 {
			img = v.Enclosure[0].URL
		}

		var message string
		if v.Title == v.Description {
			message = fmt.Sprintf("快讯：%s %s", v.Title, link)
		} else {
			message = fmt.Sprintf("【%s】%s %s", v.Title, v.Description, link)
		}

		message = fmt.Sprintf(
			"%s\n\n"+
				"ссылка на новость:\n<code>%s</code>\n"+
				"фото:\n<code>%s</code>", message, v.Link, img)

		tgPost := TgPost{
			Message:   message,
			Link:      v.Link,
			ShortLink: linkShort,
			Img:       img,
		}

		err = SendTelegram(&tgPost)
		if err != nil {
			fmt.Println(fmt.Sprintf("error send telegram err=%s post=%+v", err, tgPost))
		}

		if err := DB.Set(ctx, v.Link, fmt.Sprintf("%+v", v), 0).Err(); err != nil {
			fmt.Printf("redis is err=%s\n", err)
		}
	}
}

func SendTelegram(m *TgPost) error {
	if global.TG_CHAT == 0 {
		return fmt.Errorf("not valid chat_id")
	}
	t := TelegramClient

	methodType := "sendMessage"
	message := sendMessageReq{
		ChatId: global.TG_CHAT,
		Mode:   "HTML",
	}

	if m.Img != "" {
		methodType = "sendPhoto"
		message.Photo = m.Img
		message.Caption = m.Message
	} else {
		message.Text = m.Message
	}

	req := requests.Request{
		Method:   http.MethodPost,
		Uri:      methodType,
		JsonBody: &message,
		Flags: requests.RequestFlags{
			IsBodyString: true,
		},
	}
	res := requests.Response{}
	err := t.NewRequest(&req, &res)
	if err != nil {
		return err
	}

	if res.Code != 200 {
		return fmt.Errorf("error code=%d body=%s", res.Code, res.Body)
	}

	return nil
}

func GetRss(r *Rss) error {
	req := requests.Request{Method: http.MethodGet}
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
	err := SputnikShortLinkClient.NewRequest(&req, &res)

	return res.Body, err
}
