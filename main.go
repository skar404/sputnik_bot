package main

import (
	"os"

	"sputnik_bok/weibo"
)

func main() {
	login := os.Getenv("LOGIN")
	pass := os.Getenv("PASS")

	weibo.NewConfig().Login(login, pass)
}
