package global

import (
	"os"
	"strconv"
)

var (
	TG_TOKEN                = os.Getenv("TG_TOKEN")
	TG_CHAT, _              = strconv.Atoi(os.Getenv("TG_CHAT"))
	SPUTNIK_SHORT_LINK_URL  = os.Getenv("SPUTNIK_SHORT_LINK_URL")
	DB_HOST                 = getEnv("DB_HOST", "localhost:6370")
	SHORT_LINK_TOKEN        = os.Getenv("SHORT_LINK_TOKEN")
	SHORT_LINK_GROUP_GUID   = os.Getenv("SHORT_LINK_GROUP_GUID")
	SHORT_LINK_GROUP_DOMAIN = getEnv("SHORT_LINK_GROUP_DOMAIN", "bit.ly")
)

func getEnv(key, fallback string) string {
	value := os.Getenv(key)
	if len(value) == 0 {
		return fallback
	}
	return value
}
