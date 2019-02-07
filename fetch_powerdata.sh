db="power"
sql="select time,host,value from Power where time > now()-$1"
./influxQuery.sh "$db" "$sql"
