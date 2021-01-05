package main

import (
	"context"
	"fmt"
	"log"
	"time"

	"github.com/go-redis/redis/v8"

	"github.com/skar404/sputnik_bot/bitly"
	"github.com/skar404/sputnik_bot/global"
	"github.com/skar404/sputnik_bot/sputnik"
	"github.com/skar404/sputnik_bot/telegram"
)

var DB = redis.NewClient(&redis.Options{
	Addr:     global.DB_HOST,
	Password: "", // no password set
	DB:       0,  // use default DB
})

func main() {
	log.Println("Start app")

	index := 0

	for true {
		rssFeed := sputnik.Rss{}
		err := sputnik.GetRss(&rssFeed)
		if err != nil {
			fmt.Sprintln(err)
		}
		Notification(&rssFeed)

		if (index % 10) == 0 {
			log.Printf("global 15s sleep ... index=%d\n", index)
		}
		time.Sleep(15 * time.Second)
		index += 1
	}
}

func Notification(r *sputnik.Rss) {
	for _, v := range r.Channel.Item {
		ctx := context.Background()
		if v.Link == "" {
			log.Println(fmt.Sprintf("error get short item=%+v", v))
			continue
		}

		val, err := DB.Get(ctx, v.Link).Result()
		if err == redis.Nil {
			log.Printf("new post link=%s\n", v.Link)
		} else if err != nil {
			log.Printf("redis is err=%s\n", err)
			continue
		}

		if val != "" {
			continue
		}

		linkShort, err := sputnik.GetShortLink(v.Link)
		if err != nil {
			log.Println(fmt.Sprintf("error sputnik get short link err=%s", err))
		}

		if linkShort == "" {
			linkShort, err = bitly.CreateLink(v.Link)

			if err != nil {
				log.Println(fmt.Sprintf("error bitly get short link err=%s", err))
			}
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
		var lightningText string

		if v.Title == v.Description || v.Title == "" || v.Description == "" {
			if v.Title != "" {
				lightningText = v.Title
			} else if v.Description != "" {
				lightningText = v.Description
			}
		}

		if v.Link == "http://sputniknews.cn/economics/202101061032834250/" {
			println()
		}

		if lightningText != "" {
			message = fmt.Sprintf("快讯：%s %s", lightningText, link)
		} else {
			message = fmt.Sprintf("【%s】%s %s", v.Title, v.Description, link)
		}

		message = fmt.Sprintf(
			"%s\n\n"+
				"ссылка на новость:\n<code>%s</code>", message, v.Link)

		if img != "" {
			message += fmt.Sprintf("\nфото:\n<code>%s</code>", img)
		}

		tgPost := telegram.TgPost{
			Message: message,
			Img:     img,
		}

		err = telegram.SendTelegram(&tgPost)
		if err != nil {
			log.Println(fmt.Sprintf("error send telegram err=%s post=%+v", err, tgPost))

			log.Println("telegram 15s sleep ...")
			time.Sleep(15 * time.Second)
		}

		if err := DB.Set(ctx, v.Link, fmt.Sprintf("%+v", v), 0).Err(); err != nil {
			log.Printf("redis is err=%s\n", err)
		}
	}
}
