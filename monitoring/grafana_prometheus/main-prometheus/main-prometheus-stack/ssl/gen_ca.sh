#!/bin/sh

# Generate for Grafana
openssl req \
  -new \
  -newkey rsa:4096 \
  -days 3650 \
  -nodes \
  -x509 \
  -subj "/C=RU/ST=RU/L=Kazan/O=Grafana ingress/CN=monitoring.robolab.innopolis.university" \
  -keyout monitoring.key \
  -out monitoring.pem