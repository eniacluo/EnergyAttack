time="`date '+%Y-%m-%d %T.%3N'`"

echo "Start Time: "$time
"$@"
echo -e $time"\t$@" >> history

time="`date '+%Y-%m-%d %T.%3N'`"
echo "End Time: "$time
echo -e $time"\tEnd." >> history
