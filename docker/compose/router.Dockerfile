FROM compose-base:latest

COPY ./docker/compose/router.ini /root/.arqnet/arqnet.ini

CMD ["/arqnet"]
EXPOSE 1090/udp 1190/tcp
