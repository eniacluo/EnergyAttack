./ssh_pi.sh A sudo mv /etc/network/interfaces /etc/network/interfaces.mesh
./ssh_pi.sh A sudo mv /etc/network/interfaces.backup /etc/network/interfaces
#./ssh_pi.sh A sudo ifdown wlan0
#./ssh_pi.sh A sudo ifup wlan0
./ssh_pi.sh A sudo reboot
