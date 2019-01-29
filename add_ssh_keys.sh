# ssh-keygen -t rsa
user=pi; ip=172.22.114.74
for ip in 83 84 85 86 89 90 91 92
do
    ssh $user@"172.22.114."$ip mkdir -p .ssh
    cat ~/.ssh/id_rsa.pub | ssh $user@$"172.22.114."$ip 'cat >> .ssh/authorized_keys'
done

