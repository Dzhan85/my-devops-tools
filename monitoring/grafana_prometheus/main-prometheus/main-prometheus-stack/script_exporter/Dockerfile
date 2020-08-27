FROM alpine:latest

RUN apk --update add --no-cache python3
COPY --from=adhocteam/script-exporter:master /bin/script-exporter /bin/script-exporter
COPY --from=adhocteam/script-exporter:master /etc/script-exporter/config.yml  /etc/script-exporter/config.yml

EXPOSE 9172/tcp
ENTRYPOINT ["/bin/script-exporter"]
CMD ["-config.file=/etc/script-exporter/config.yml"]
