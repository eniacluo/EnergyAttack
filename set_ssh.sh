if [ $# -lt 2 ]
then
    echo "username and ip/hostname needed."
    exit 1
fi

user=$1; ip=$2

if [ ! -e $HOME/.ssh/id_rsa.pub ]
then
    echo "id_rsa.pub not exists. Create now: Enter x3."
    ssh-keygen -t rsa    
fi

ssh $user@$ip mkdir -p .ssh

cat ~/.ssh/id_rsa.pub | ssh $user@$ip 'cat >> .ssh/authorized_keys'
