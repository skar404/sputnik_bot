package main

import (
	"os"

	"sputnik_bok/app/client/weibo"
)

func main() {
	login := os.Getenv("LOGIN")
	pass := os.Getenv("PASS")

	weibo.NewConfig().Login(login, pass)
}
