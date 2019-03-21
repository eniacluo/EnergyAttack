#!/bin/sh

cd ..
./fetch_powerdata.sh 120s > latest.dat
mv latest.dat raw_data/realtime/
cd raw_data/realtime
./sep.sh latest