if [ $# -lt 2 ]
then
    echo "Usage: ssh_pi.sh <Group file> <cmd>"
    exit 1
fi

if [ ! -e $1 ]    # if specified a group file name
then 
    echo "There is not Group file named $1!"
    exit 2
else
    cmd="${@:2}"
    group=$(cat $1)
fi

for i in $group
    do echo "--- This is pi$i ---" 
    ssh pi@pi$i "$cmd"
done
