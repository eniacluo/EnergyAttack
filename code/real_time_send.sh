#!/bin/sh

curl -i -XPOST 'http://localhost:8086/write?db=power' --data-binary "demo,tag=label value=$1 $(date +%s%N)" >/dev/null 2>/dev/null
curl -i -XPOST 'http://localhost:8086/write?db=power' --data-binary "demo,tag=proba value=$2 $(date +%s%N)" >/dev/null 2>/dev/null
curl -i -XPOST 'http://localhost:8086/write?db=power' --data-binary "demo,tag=probb value=$3 $(date +%s%N)" >/dev/null 2>/dev/null