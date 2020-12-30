FROM golang:1.15-alpine as builder

WORKDIR /app

COPY go.mod go.sum /app/
RUN go mod download

COPY . .
RUN go build -o bin/sputnik_bot

FROM alpine

RUN apk --no-cache add ca-certificates

WORKDIR /root/

COPY --from=builder /app/bin/sputnik_bot /usr/local/bin/

EXPOSE 1323

CMD ["sputnik_bot"]