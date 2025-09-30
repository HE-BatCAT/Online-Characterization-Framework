#!/bin/bash
set -euo pipefail

INFLUXDB_URL=${INFLUXDB_URL:-"http://influxdb:8181"}
DATABASE_NAME=${DATABASE_NAME:-"Default"}
OPTS=("-H" "${INFLUXDB_URL}")

echo "Connect to InfluxDB"
until curl -s ${INFLUXDB_URL}/ping
do
    echo ...
    sleep 1
done
echo


echo
echo "Show databases"
influxdb3 show databases "${OPTS[@]}" --format csv | tail -n +2 | tee /tmp/.databases | sed -e 's/^..*/ - \0/'


if grep -c "$DATABASE_NAME" /tmp/.databases
then
    echo "Found ${DATABASE_NAME}"
else
    echo
    echo "Create database ${DATABASE_NAME}"
    influxdb3 create database "${OPTS[@]}" "$DATABASE_NAME"
fi


