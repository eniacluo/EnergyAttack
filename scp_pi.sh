if [ $# != 3 ]
then
    echo "Usage: scp_pi.sh <Group file> <src> <dst>"
    exit 1
fi

src=$2
dst=$3

if [ ! -e $1 ]    # if specified a group file name
then 
    echo "There is not Group file named $1!"
    exit 2
else
    group=$(cat $1)
fi

for i in $group
do 
    echo "--- This is pi$i ---" 
    scp "$src" pi@pi$i:"$dst"
done
