db="collectd"
sql="select time,host,value from cpu_value where time > now()-$1"
./influxQuery.sh "$db" "$sql"
