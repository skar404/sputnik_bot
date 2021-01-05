package telegram

import (
	"fmt"
	"net/http"
	"time"

	"github.com/skar404/sputnik_bot/global"
	"github.com/skar404/sputnik_bot/requests"
)

var Client = requests.RequestClient{
	Url:     fmt.Sprintf("https://api.telegram.org/bot%s/", global.TG_TOKEN),
	Timeout: 10 * time.Second,
	Header: map[string][]string{
		"Content-Type": {"application/json"},
		"charset":      {"utf-8"},
	},
}

type TgPost struct {
	Message string
	Img     string
	Video   string
}

type smartMessageReq struct {
	ChatId int    `json:"chat_id"`
	Mode   string `json:"parse_mode"`
	Text   string `json:"text,omitempty"`

	Caption string `json:"caption,omitempty"`
	Photo   string `json:"photo,omitempty"`
	Video   string `json:"video,omitempty"`
}

func SendTelegram(m *TgPost) error {
	if global.TG_CHAT == 0 {
		return fmt.Errorf("not valid chat_id")
	}
	t := Client

	methodType := "sendMessage"
	message := smartMessageReq{
		ChatId: global.TG_CHAT,
		Mode:   "HTML",
	}

	if m.Video != "" {
		methodType = "sendVideo"
		message.Video = m.Video
		message.Caption = m.Message
	} else if m.Img != "" {
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
		// {"ok":false,"error_code":400,"description":"Bad Request: wrong file identifier/HTTP URL specified"}
		// {"ok":false,"error_code":400,"description":"Bad Request: wrong file identifier/HTTP URL specified"}
		return fmt.Errorf("error code=%d body=%s", res.Code, res.Body)
	}

	return nil
}
