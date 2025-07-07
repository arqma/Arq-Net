ARG bootstrap="https://i2p.rocks/i2procks.signed"
FROM alpine:edge as builder

RUN apk update && \
    apk add build-base cmake git libcap-dev libcap-static libuv-dev libuv-static curl ninja bash binutils-gold curl-dev

WORKDIR /src/
COPY . /src/

RUN make NINJA=ninja STATIC_LINK=ON BUILD_TYPE=Release DOWNLOAD_SODIUM=ON
RUN ./arqnet-bootstrap ${bootstrap}

FROM alpine:latest

COPY arqnet-docker.ini /root/.arqnet/arqnet.ini
COPY --from=builder /src/build/daemon/arqnet .
COPY --from=builder /root/.arqnet/bootstrap.signed /root/.arqnet/

CMD ["./arqnet"]
EXPOSE 1090/udp 1190/tcp
