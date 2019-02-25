./ssh_pi.sh A sudo mv /etc/network/interfaces /etc/network/interfaces.backup
./ssh_pi.sh A sudo mv /etc/network/interfaces.mesh /etc/network/interfaces
#./ssh_pi.sh A sudo ifdown wlan0
#./ssh_pi.sh A sudo ifup wlan0
./ssh_pi.sh A sudo reboot
