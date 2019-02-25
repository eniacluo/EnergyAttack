./ssh_pi.sh A "ps aux | grep python | grep -v grep | awk '{print \$2, \$11, \$12}'"
