if [ $1 = '-n' ]    # specify one device
then
    group=$2
    cmd="${@:3}"
else                # specify a file contains a group
    cmd="${@:2}"
    if [ ! -e $1 ]    # if specified a group file name
    then 
        echo "There is not Group file named $1!"
        exit 1
    else
        group=$(cat $1)
    fi
fi

for i in $group
    do echo "--- This is pi$i ---" 
    ssh pi@pi$i "$cmd"
done
