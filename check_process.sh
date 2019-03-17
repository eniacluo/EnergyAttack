./ssh_pi.sh B "ps aux | grep python | grep -v grep | awk '{print \$2, \$11, \$12}'"
