FROM golang:1.24-alpine AS builder

WORKDIR /build

COPY go.mod .

RUN go mod download

COPY . .

RUN go build -o main .

FROM scratch

WORKDIR /build

COPY --from=builder /build .

EXPOSE 8080

CMD [ "./main" ]