nmap -sP 10.42.0.* > tmp

for i in $(cat A) $(cat B)
do
    ison=`cat tmp | grep "pi$i" | cut -f 5 -d ' '`
    if [ ! -z $ison ]
    then
        echo $ison" is on."
    fi
done
rm tmp
