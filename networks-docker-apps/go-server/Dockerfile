FROM golang:1.21 AS builder

WORKDIR /app
COPY go.mod ./
COPY main.go ./
RUN go mod download
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o server

FROM alpine:latest AS finish

WORKDIR /root
COPY --from=builder /app/server .
EXPOSE 8080
CMD [ "./server" ]