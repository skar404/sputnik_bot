package global

import (
	"os"
	"strconv"
)

var (
	TG_TOKEN               = os.Getenv("TG_TOKEN")
	TG_CHAT, _             = strconv.Atoi(os.Getenv("TG_CHAT"))
	SPUTNIK_SHORT_LINK_URL = os.Getenv("SPUTNIK_SHORT_LINK_URL")
)

func getEnv(key, fallback string) string {
	value := os.Getenv(key)
	if len(value) == 0 {
		return fallback
	}
	return value
}
