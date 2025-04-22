FROM golang:1.21 AS builder

WORKDIR /app

COPY go.mod ./
COPY main.go ./

RUN go mod download

RUN GOOS=linux GOARCH=amd64 go build -o meuapp

FROM alpine:latest AS finish

WORKDIR /root

COPY --from=builder /app/meuapp .

CMD [ "./meuapp" ]