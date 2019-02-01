./scp_pi.sh collectd.conf /home/pi/
./ssh_pi.sh sudo mv collectd.conf /etc/collectd/collectd.conf
./ssh_pi.sh sudo service collectd restart

