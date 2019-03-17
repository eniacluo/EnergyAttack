#!/bin/sh

if [ $# -lt 1 ]
then
	echo "Usage 1: ./fetch_powerdata.sh <time range>"
	echo "Usage 2: ./fetch_powerdata.sh <start time> <end time>"
	exit
fi

if [ $# -eq 1 ]
then
	sql="select time,host,value from Power where time > now()-$1"
else
	sql="select time,host,value from Power where time > '$1' tz('America/EST') and time < '$2' tz('America/EST')"	
fi
db="power"
./influxQuery.sh "$db" "$sql"
