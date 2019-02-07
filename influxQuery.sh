curl -G "http://localhost:8086/query?pretty=true&db=$1&epoch=ms" --data-urlencode "q=$2" > queryResult 2>/dev/null

test=$(cat queryResult | grep values)
if [ -n "$test" ]
then
    cat queryResult | jq '[.results[].series[].values[] | {host: .[1], time: .[0], value: .[2]}]'\
        > midResult
    cat midResult | grep time | cut -f2 -d':' | cut -f1 -d',' > time
    cat midResult | grep host | cut -f2 -d':' | cut -f1 -d',' > host
    cat midResult | grep value | cut -f2 -d':' | cut -f1 -d',' > value
    paste -d',' time value host
    rm time host value
    rm midResult
fi

rm queryResult
# cat lastoneday.dat | grep pc012 | cut -f1-2 -d',' > onlydata
