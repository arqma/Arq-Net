FROM compose-base:latest

ENV ARQNET_NETID=docker

COPY ./docker/compose/bootstrap.ini /root/.arqnet/arqnet.ini

CMD ["/arqnet"]
EXPOSE 1090/udp 1190/tcp
