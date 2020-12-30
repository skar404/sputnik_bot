package main

import (
	"context"
	"fmt"
	"log"
	"time"

	"github.com/go-redis/redis/v8"

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

	for true {
		rssFeed := sputnik.Rss{}
		err := sputnik.GetRss(&rssFeed)
		if err != nil {
			fmt.Sprintln(err)
		}
		Notification(&rssFeed)

		log.Println("global 15s sleep ...")
		time.Sleep(15 * time.Second)
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
			log.Println(fmt.Sprintf("error get short link err=%s", err))
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

		tgPost := telegram.TgPost{
			Message:   message,
			Link:      v.Link,
			ShortLink: linkShort,
			Img:       img,
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
